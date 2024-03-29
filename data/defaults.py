DEFAULT_PARAMS = {
  "general": {
    "coal_must_run": [  # values change due to decommissioning of plants.
      # TODO: add comment which plant decommissioning accounts for each line
      {"start_year": 2020, "end_year": 2021, "interpo":  {"type": "constant", "value": 2440.0}},
      {"start_year": 2021, "end_year": 2022, "interpo":  {"type": "constant", "value": 2380.0}},
      {"start_year": 2022, "end_year": 2023, "interpo":  {"type": "constant", "value": 1620.0}},
      {"start_year": 2023, "end_year": 2024, "interpo":  {"type": "constant", "value": 1500.0}},
      {"start_year": 2024, "end_year": 2040, "interpo":  {"type": "constant", "value": 1440.0}},
      {"start_year": 2040, "end_year": 2045, "interpo":  {"type": "constant", "value": 960.0}},
      {"start_year": 2045, "end_year": 2049, "interpo":  {"type": "constant", "value": 480.0}},
      {"start_year": 2049, "end_year": 2050, "interpo":  {"type": "constant", "value": 0.0}}
    ]
  },
  "costs": {
    "solar": {  # PV-Average. TODO: add detailed prices and distribution per PV type as params
      "capex": [
        {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 3912, "end_value": 3274}},
        {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 3274, "end_value": 2669}},
        {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 2669, "end_value": 2368}},
        {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 2368, "end_value": 2503}},
        {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 2503, "end_value": 2312}},
        {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 2312, "end_value": 2166}}
      ],
      "opex": [
        {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 62, "end_value": 55}},
        {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 55, "end_value": 46}},
        {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 46, "end_value": 41}},
        {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 41, "end_value": 40}},
        {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 40, "end_value": 37}},
        {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 37, "end_value": 34}}
      ],
      "variable_opex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 0}}
      ],
      "lifetime": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 25}}
      ]
    },
    "wind": {
      "capex": [
        {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 4600, "end_value": 4240}},
        {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 4240, "end_value": 4000}},
        {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 4000, "end_value": 3860}},
        {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 3860, "end_value": 3760}},
        {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 3760, "end_value": 3660}},
        {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 3600, "end_value": 3600}}
      ],
      "opex": [
        {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 92, "end_value": 84}},
        {"start_year": 2025, "end_year": 2040, "interpo": {"type": "linear", "start_value": 84, "end_value": 72}},
        {"start_year": 2040, "end_year": 2050, "interpo": {"type": "constant", "value": 72}}
      ],
      "variable_opex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 0}}
      ],
      "lifetime": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 25}}
      ]
    },
    "storage": {
      "capex": [
        {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 1004.0, "end_value": 652.6}},
        {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 652.6, "end_value": 471.9}},
        {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 471.9, "end_value": 371.5}},
        {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 371.5, "end_value": 321.3}},
        {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 321.3, "end_value": 281.1}},
        {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 281.1, "end_value": 261.0}}
      ],
      "opex": [
        {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 15.6, "end_value": 12.8}},
        {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 12.8, "end_value": 10.8}},
        {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 10.8, "end_value": 9.6}},
        {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 9.6, "end_value": 8.8}},
        {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 8.8, "end_value": 8.4}},
        {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 8.4, "end_value": 8}}
      ],
      "variable_opex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 0}}
      ],
      "lifetime": [
        {"start_year": 2020, "end_year": 2030, "interpo": {"type": "constant", "value": 15}},
        {"start_year": 2030, "end_year": 2050, "interpo": {"type": "constant", "value": 20}}
      ]
    },
    "gas": {  # CCGT
      "capex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 3785}}
      ],
      "opex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 164}}
      ],
      "variable_opex": [  # var opex + fuel
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 0.0139 + 0.1176}}
      ],
      "lifetime": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 35}}
      ]
    },
    # TODO: those parameters are copied over from gas. Add the correct parameters.
    "coal": {  # CCGT
      "capex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 3785}}
      ],
      "opex": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 164}}
      ],
      "variable_opex": [  # var opex + fuel
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 0.0139 + 0.1176}}
      ],
      "lifetime": [
        {"start_year": 2020, "end_year": 2050, "interpo": {"type": "constant", "value": 35}}
      ]
    },
  },
  "emissions": {
    "gas": {
      # TODO: use the YoY change as parameters instead of the prices
      "CO2": 0.397,
      "SOx": 0,
      "NOx": 0.00016,
      "PMx": 0.00002

    },
    # TODO: those aren't good sources
    # * Air Pollutant Emission Abatement of the Fossil-Fuel Power
    #   Plants by Multiple Control Strategies in Taiwan
    # * https://www.eia.gov/tools/faqs/faq.php?id=74&t=11
    "coal": {
      "CO2": 1.011,
      "SOx": 0.0003322,
      "NOx": 0.0002587,
      "PMx": 0.0000358
    }
  },
  "emissions_costs": {
    "CO2": [
      {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 0.167, "end_value": 0.185}},
      {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 0.185, "end_value": 1.206}},
      {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 0.206, "end_value": 0.226}},
      {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 0.226, "end_value": 0.248}},
      {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 0.248, "end_value": 0.269}},
      {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 0.269, "end_value": 0.291}}
    ],
    "SOx": [
      {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 85.381, "end_value": 100.868}},
      {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 100.868, "end_value": 119.164}},
      {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 119.164, "end_value": 139.086}},
      {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 139.086, "end_value": 162.337}},
      {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 162.337, "end_value": 189.476}},
      {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 189.476, "end_value": 221.151}}
    ],
    "NOx": [
      {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 118.208, "end_value": 139.650}},
      {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 139.650, "end_value": 164.980}},
      {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 164.980, "end_value": 192.561}},
      {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 192.561, "end_value": 224.752}},
      {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 224.752, "end_value": 262.325}},
      {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 262.325, "end_value": 306.179}}
    ],
    "PMx": [
      {"start_year": 2020, "end_year": 2025, "interpo": {"type": "linear", "start_value": 270.760, "end_value": 319.873}},
      {"start_year": 2025, "end_year": 2030, "interpo": {"type": "linear", "start_value": 319.873, "end_value": 377.894}},
      {"start_year": 2030, "end_year": 2035, "interpo": {"type": "linear", "start_value": 377.894, "end_value": 441.068}},
      {"start_year": 2035, "end_year": 2040, "interpo": {"type": "linear", "start_value": 441.068, "end_value": 514.803}},
      {"start_year": 2040, "end_year": 2045, "interpo": {"type": "linear", "start_value": 514.803, "end_value": 600.865}},
      {"start_year": 2045, "end_year": 2050, "interpo": {"type": "linear", "start_value": 600.865, "end_value": 701.314}}
    ]
  }
}
