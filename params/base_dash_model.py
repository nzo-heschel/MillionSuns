import base64
import json
import typing as t
from secrets import token_hex

import dash_ace
import dash_bootstrap_components as dbc
from dash import Input, Output, State, ctx, dcc
from pydantic import BaseModel

if t.TYPE_CHECKING:
    from dash import Dash
    from pydantic.fields import ModelField
    from dash.development.base_component import Component


def comp_id(s: str) -> str:
    return f'bdm__{s}__{token_hex(8)}'


def deep_model_update(model: 'BaseDashModel', update_dict: dict[str, t.Any]):
    for k, v in update_dict.items():
        setattr(
            model,
            k,
            deep_model_update(getattr(model, k), v)
            if isinstance(v, dict)
            else v
        )
    return model


class BaseDashModel(BaseModel):
    def __input(self, app: 'Dash', field: 'ModelField', update_btn_id: str, **kwargs):
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

    def __labeled_input(self, app: 'Dash', field: 'ModelField', update_btn_id: str, **kwargs):
        return dbc.Container(
            [
                dbc.Label(
                    class_name='mt-2',
                    children=field.field_info.title
                ),
                self.__input(
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
        if issubclass(field.type_, BaseDashModel):
            return getattr(self, field.name).dash(
                app,
                field.field_info.title or field.name.replace('_', ' ').title(),
                field.field_info.description,
                update_btn_id
            )
        elif issubclass(field.type_, int):
            return self.__labeled_input(
                app,
                field,
                update_btn_id,
                type='number',
                step=1
            )
        elif issubclass(field.type_, float):
            return self.__labeled_input(
                app,
                field,
                update_btn_id,
                type='number',
                step=0.005
            )

    def dash(self, app: 'Dash', title: str, desc: str, update_btn_id: str):
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
                    children=list(
                        map(
                            lambda field: self._component(app, field, update_btn_id),
                            self.__fields__.values()
                        )
                    )
                )
            ],
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
                        self.dash(
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
