

HEADERS = {
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.767 Yowser/2.5 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
}

tanks = []

async def get_ttc(session, tier, nation, name, vehicle_cd):
    global tanks

    params = {
        'filter[language]': 'ru',
        'filter[vehicle_cd]': vehicle_cd
    }
    
    async with session.get(
        'https://tanki.su/wotpbe/tankopedia/api/vehicle/modules/',
        params=params,
        headers=HEADERS
    ) as response:
        response = await response.json()

    configures = response["data"]['binds'].keys()
    modules = response["data"]['modules']

    top_configure = {
        'vehicleTurret': [],
        'vehicleGun': [],
        'vehicleChassis': [],
        'vehicleEngine': [],
        'vehicleRadio': []
    }

    for module_id in modules.keys():

        module_type = modules[module_id]['type']
        module_lvl = modules[module_id]['level']

        if all(module_lvl > modules[i]['level'] for i in top_configure[module_type]):
            top_configure[module_type] = [module_id]

        elif all(module_lvl == modules[i]['level'] for i in top_configure[module_type]):
            top_configure[module_type].append(module_id)

    top_configure = top_configure['vehicleTurret'] + top_configure['vehicleChassis'] + top_configure['vehicleEngine'] + \
                    top_configure['vehicleRadio'] + top_configure['vehicleGun']

    data = []
    for configure_id in configures:

        configure = response["data"]['binds'][configure_id]
        configure_str = '; '.join([modules[i]['mark'] for i in configure_id.split('-')])
        ttc = configure['ttc']

        if all(i in top_configure for i in configure_id.split('-')):
            status = 'Top'

        elif configure.get('is_default', False) == True:
            status = 'Default'

        else:
            status = 'intermediate'

        data.append(
            [
                tier, nation, name, status, configure_str,
                ttc.get('piercing1', 0), ttc.get('piercing2', 0), ttc.get('piercing3', 0),
                ttc.get('damage1', 0), ttc.get('damage2', 0), ttc.get('damage3', 0),
                ttc.get('reload_time', 0), ttc.get('autoreload_reload_time', 0), ttc.get('clip_rate', 0),
                ttc.get('clip_count', 0), ttc.get('gun_rate', 0), ttc.get('damage_per_minute', 0),
                ttc.get('aiming_time', 0), ttc.get('shot_dispersion_radius', 0), ttc.get('max_health', 0),
                ttc.get('hull_armor_forehead', 0), ttc.get('hull_armor_board', 0), ttc.get('hull_armor_feed', 0),
                ttc.get('turret_armor_forehead', 0), ttc.get('turret_armor_board', 0), ttc.get('turret_armor_feed', 0),
                ttc.get('weight', 0), ttc.get('power_weight_ratio', 0), ttc.get('speed_forward_kmh', 0),
                ttc.get('speed_back_kmh', 0), ttc.get('chassis_rotation_speed_deg', 0),
                ttc.get('turret_rotation_speed_deg', 0), ttc.get('circular_vision_radius', 0),
            ]
        )
    tanks += data




