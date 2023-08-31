import asyncio
import pandas as pd
from tasks import get_tasks
from ttc import tanks

HEADER = [
        'Level', 'Nation', 'Name', 'Status', 'Configure', 'Piercing1', 'Piercing2', 'Piercing3',
        'Damage1', 'Damage2', 'Damage3', 'Reload time', 'Autoreload time', 'Clip rate',
        'Clip count', 'Gun rate', 'DPM', 'Aiming time', 'Shot dispersion radius',
        'Health', 'Hull armor forehead', 'Hull armor board', 'hull armor aft',
        'Turret armor forehead', 'turret armor board', 'Turret armor aft',
        'Weight', 'Power weight ratio', 'Speed forward kmh', 'Speed back kmh',
        'Chassis rotation speed deg', 'turret rotation speed deg', 'circular vision radius'
    ]

def main():
    asyncio.run(get_tasks())
    df = []
    for tank in sorted(tanks):
        tank[12] = ' / '.join(list(map(str, tank[12])))
        if not tank[12]: tank[12] = 0
        df.append(tank)
    df = pd.DataFrame(df)
    df.to_excel('wot_tanks.xlsx', index=False, header=HEADER)
    
    print(df)

main()
    
