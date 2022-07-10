import base64
import inspect
import json
import typing as t
from secrets import token_hex

import dash_ace
import dash_bootstrap_components as dbc
import typing_inspect as ti
from dash import Input, MATCH, Output, State, ctx, dcc
from pydantic import BaseModel as PydanticBaseModel, PrivateAttr
from pydantic.fields import ModelField
from pydantic.generics import GenericModel

if t.TYPE_CHECKING:
    from dash import Dash
    from dash.development.base_component import Component


def comp_id(s: str) -> str:
    return f'bdm__{s}__{token_hex(8)}'


def deep_model_update(model: 'BaseModel', update_dict: dict[str, t.Any]):
    for k, v in update_dict.items():
        setattr(
            model,
            k,
            deep_model_update(getattr(model, k), v)
            if isinstance(v, dict)
            else v
        )
    return model


class BaseModel(PydanticBaseModel):
    @staticmethod
    def _label(title: str):
        return dbc.Label(
            class_name='mt-2',
            children=title
        )

    def _input(self, app: 'Dash', field: 'ModelField', update_btn_id: str, **kwargs):
        inp_id = comp_id('input')

        @app.callback(
            Output(inp_id, 'key'),
            Input(inp_id, 'value')
        )
        def int_update(value: t.Any):
            setattr(self, field.name, value)
            return inp_id

        @app.callback(
            Output(inp_id, 'value'),
            Input(update_btn_id, 'n_clicks')
        )
        def ext_update(n_clicks: int):
            return getattr(self, field.name)

        return dbc.Input(
            id=inp_id,
            min=field.field_info.le or field.field_info.lt,
            max=field.field_info.ge or field.field_info.gt,
            value=getattr(self, field.name),
            **kwargs
        )

    def _labeled_input(self, app: 'Dash', field: 'ModelField', update_btn_id: str, **kwargs):
        return dbc.Container(
            [
                self._label(field.field_info.title or field.name.replace('_', ' ').title()),
                self._input(
                    app,
                    field,
                    update_btn_id,
                    **kwargs
                )
            ]
        )

    def _component(
        self,
        app: 'Dash',
        field: 'ModelField',
        update_btn_id: str
    ) -> 'Component':
        attr = getattr(self, field.name)

        try:
            if ti.is_literal_type(field.type_):
                return dbc.Container()
            elif issubclass(field.type_, int):
                return self._labeled_input(
                    app,
                    field,
                    update_btn_id,
                    type='number',
                    step=1
                )
            elif issubclass(field.type_, float):
                return self._labeled_input(
                    app,
                    field,
                    update_btn_id,
                    type='number',
                    step=0.005
                )
            elif issubclass(field.type_, BaseModel):
                return attr.dash_collapse(
                    app,
                    field.field_info.title or field.name.replace('_', ' ').title(),
                    field.field_info.description,
                    update_btn_id
                )
            else:
                raise NotImplementedError(f'The type {field.type_!r} is not yet supported')
        except TypeError as e:
            raise NotImplementedError(f'The type {field.type_!r} is not yet supported') from e

    def dash_fields(
        self,
        app: 'Dash',
        update_btn_id: str
    ) -> 'Component':
        return dbc.Container(
            list(
                map(
                    lambda field: self._component(app, field, update_btn_id),
                    self.__fields__.values()
                )
            )
        )

    def dash_collapse(
        self,
        app: 'Dash',
        title: str,
        desc: str,
        update_btn_id: str
    ) -> 'Component':
        raise NotImplementedError()


class DashModel(BaseModel):
    def dash_collapse(
        self,
        app: 'Dash',
        title: str,
        desc: str,
        update_btn_id: str
    ) -> 'Component':
        btn_id = comp_id('collapse_btn')
        coll_id = comp_id('collapse')

        @app.callback(
            Output(coll_id, 'is_open'),
            Input(btn_id, 'n_clicks'),
            State(coll_id, 'is_open'),
            prevent_initial_call=True
        )
        def update_collapse(n_clicks: int, is_open: bool):
            return not is_open

        return dbc.Card(
            class_name='p-3 m-3',
            children=[
                dbc.Button(
                    id=btn_id,
                    children=title
                ),
                dbc.Container(class_name='text-muted text-center', children=desc),
                dbc.Collapse(
                    id=coll_id,
                    children=self.dash_fields(app, update_btn_id)
                )
            ]
        )

    def dash_editor(
        self,
        app: 'Dash',
        title: str,
        desc: str
    ) -> 'Component':
        ui_tab = comp_id('ui_tab')
        json_sub = comp_id('json_sub')
        json_up = comp_id('json_up')
        json_down_btn = comp_id('json_down_btn')
        json_down = comp_id('json_down')
        json_ref = comp_id('json_ref')
        json_ace = comp_id('json_ace')

        @app.callback(
            Output(json_sub, 'key'),  # just need some output
            Input(json_sub, 'n_clicks'),
            State(json_ace, 'value')
        )
        def update_from_json(n_clicks: int, value: str):
            if value != self.json(indent=4):
                deep_model_update(self, json.loads(value))
            return self.json()

        @app.callback(
            Output(json_ace, 'value'),
            Input(json_up, 'contents'),
            Input(json_ref, 'n_clicks'),
            prevent_initial_call=True
        )
        def upload_params_jsons(content: str, n_clicks: int):
            if ctx.triggered_id == json_up and content:
                _, content_encoded = content.split(',')
                return base64.b64decode(content_encoded).decode('utf-8')

            if ctx.triggered_id == json_ref:
                return self.json(indent=4)

        @app.callback(
            Output(json_down, 'data'),
            Input(json_down_btn, 'n_clicks'),
            State(json_ace, 'value'),
            prevent_initial_call=True
        )
        def download_params_jsons(n_clicks: int, value: str):
            return dcc.send_string(value, f'{title}.json', 'text/json')

        return dbc.Tabs(
            children=[
                dbc.Tab(
                    id=ui_tab,
                    label='UI Editor',
                    children=[
                        self.dash_collapse(
                            app,
                            title,
                            desc,
                            json_sub
                        )
                    ]
                ),
                dbc.Tab(
                    label='JSON Editor',
                    children=[
                        dbc.Container(
                            class_name='d-flex flex-row justify-content-center',
                            children=[
                                dbc.Button(
                                    id=json_sub,
                                    class_name='m-2',
                                    children='Submit'
                                ),
                                dbc.Button(
                                    id=json_ref,
                                    class_name='m-2',
                                    children='Refresh'
                                ),
                                dcc.Upload(
                                    id=json_up,
                                    className='btn btn-primary m-2',
                                    children='Upload'
                                ),
                                dbc.Button(
                                    id=json_down_btn,
                                    class_name='m-2',
                                    children='Download'
                                ),
                                dcc.Download(id=json_down)
                            ]
                        ),
                        dash_ace.DashAceEditor(
                            id=json_ace,
                            value=self.json(indent=4),
                            theme='monokai',
                            mode='json',
                            enableBasicAutocompletion=True,
                            enableLiveAutocompletion=True,
                            fontSize=18,
                            style={'font-family': 'monospace, monospace'}
                        )
                    ]
                )
            ]
        )


T = t.TypeVar('T', bound=BaseModel)


class DashSelect(BaseModel, GenericModel, t.Generic[T]):
    _options: dict[str, T] = PrivateAttr()
    _selected_name: str = PrivateAttr()
    selected: T

    def __init__(self, **data):
        super().__init__(**data)

        self._options = {
            k.strip('_').title(): getattr(self, k)
            for k in dict(inspect.getmembers(self))['__annotations__']
        }

        if self.selected:
            for name, opt in self._options.items():
                if type(self.selected) == type(opt):
                    self._selected_name = name
                    self._options[name] = self.selected
                    break
            else:
                raise ValueError(
                    'Selected option does not seem to exists.\n'
                    f'{self.selected=}\n{self._options=}'
                )

        else:
            self._selected_name, self.selected = next(iter(self._options.items()))

    def dash_collapse(self, app: 'Dash', title: str, desc: str, update_btn_id: str) -> 'Component':
        select_id = comp_id('select')
        col_id_type = comp_id('collapse')
        coll_ids = {name: {'type': col_id_type, 'name': name} for name in self._options}

        @app.callback(
            Output({'type': col_id_type, 'name': MATCH}, 'is_open'),
            Input(select_id, 'value'),
            Input(update_btn_id, 'n_clicks'),
            State({'type': col_id_type, 'name': MATCH}, 'id')
        )
        def select(value: str, n_clicks: int, col_id: dict[str, str]):
            if ctx.triggered_id == select_id:
                self.selected = self._options[value]
            return col_id['name'] == value

        return dbc.Container(
            [
                self._label(title),
                dbc.Select(
                    id=select_id,
                    options=[{'label': opt} for opt in self._options],
                    value=self._selected_name
                ),
                dbc.Card(
                    class_name='m-2 p-2',
                    children=[
                        dbc.Collapse(
                            id=coll_ids[name],
                            is_open=False,
                            children=opt.dash_fields(
                                app,
                                update_btn_id
                            )
                        )
                        for name, opt in self._options.items()
                    ]
                )
            ]
        )