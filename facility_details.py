import sqlite3
import utils

def get_install_modifiers():
    with open('./data/facility_rates.csv', 'r') as f:
        facility_info = f.read().split('/')
        system_id = int(facility_info[0])
        job_cost_modifier = float(facility_info[1])
        tax_rate = float(facility_info[2])
        
        return system_id, job_cost_modifier, tax_rate
    
def get_me_modifier(group_id):
    with open('./data/facility_rates.csv', 'r') as f:
        facility_info = f.read().split('/')
        me_bonuses = eval(facility_info[3])
        
        me_bonus = me_bonuses.get(group_id, 0)
        if me_bonus == 0:
            print("No ME bonus found for this group")

        return me_bonus

def update_facility_details():   
    tax_rate, job_cost_modifier = input_install_cost_modifiers()
    me_bonuses = input_me_bonuses()
        
    with open('./data/facility_rates.csv', 'w') as f:
        f.write(f"{utils.ELDJ_SYSTEM_ID}/{str(job_cost_modifier)}/{str(tax_rate)}/{str(me_bonuses)}")
        
def input_install_cost_modifiers():
    fac_tax = float(input("Enter the facility tax rate: "))
    scc_tax = 4.0
    tax_rate = fac_tax + scc_tax

    job_cost_modifier = float(input("Enter the job cost modifier: "))

    return tax_rate, job_cost_modifier

def input_me_bonuses():
    me_bonus_groups = {}

    struct_role_bonus = float(input("Enter the structure role bonus: "))/100
    struct_rig_bonus = float(input("Enter the structure rig bonus: "))/100

    conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
    cursor = conn.cursor()

    group = ''
    while group != 'x':
        group = input("Enter a group that is affected by the rig (x to exit): ")
        if group == 'x':
            break
        
        cursor.execute("SELECT groupID FROM invGroups WHERE groupName LIKE ?", (group,))
        group_id = cursor.fetchone()

        if group_id is None:
            print("Not a valid group name")
            continue

        me_bonus_groups.update({group_id[0]: (1-struct_rig_bonus)*(1-struct_role_bonus)})    

    cursor.execute("SELECT groupID FROM invGroups")
    all_groups = cursor.fetchall()

    for group in all_groups:
        if group[0] in me_bonus_groups:
            continue
        else:
            me_bonus_groups.update({group[0]: (1-struct_role_bonus)})
    conn.close()
    return me_bonus_groups
