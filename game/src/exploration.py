success_crit = 2
success_comp = 1
success_part = 0
failure_part = -1
failure_comp = -2
failure_crit = -3

reward = 1
risk = 2
cost = 3

d20_thresh = 10
d40_thresh = 30
d60_thresh = 50
d80_thresh = 70
d100_thresh = 90
d120_thresh = 110
d200_thresh = 200

def get_quantification_die(num):
    die = "d0"
    
    if num <= d20_thresh:
        die = "d20"
    elif num <= d40_thresh:
        die = "d40"
    elif num <= d60_thresh:
        die = "d60"
    elif num <= d80_thresh:
        die = "d80"
    elif num <= d100_thresh:
        die = "d100"
    elif num <= d120_thresh:
        die = "d120"
    elif num <= d200_thresh:
        die = "d200"
        
    return die

def get_intput(prompt):
    response = input(prompt)
    
    try:
        response = int(response)
    except ValueError as ex:
        response = 0
    
    return response

class exploration_class:
    
    def __init__(self, rm, lvl, explo, perc, eusoc):
        self.room = rm
        self.lvl = lvl
        self.explo = explo
        self.perc = perc
        self.eusoc = eusoc
        
def yes_no(answer):
    if (answer == "Y") or (answer == "y"):
        return True
    else:
        return False
    
def is_change():
    change = input("Change Skills? [Y/N]")
    return(yes_no(change))

def get_information():
    
    room = get_intput("Room ID: ")
    lvl = get_intput("Level: ")
    explo = get_intput("Exploration Rating: ")
    perc = get_intput("Perception Rating: ")
    eusoc = get_intput("Eusociology Rating: ")
    
    exp = exploration_class(
        room, lvl, explo, perc, eusoc
        )
        
    return exp

def print_result(res):
    if res >= success_crit:
        print("Critical Success!")
    elif res == success_comp:
        print("Success!")
    elif res == success_part:
        print("Partial Success.")
    elif res == failure_part:
        print("Partial Failure.")
    elif res == failure_comp:
        print("Failure.")
    elif res == failure_crit:
        print("Critical Failure!")

def roll_result(roll, effort, resistance, pos_mods, neg_mods):
    res_num = 0
    print(roll)
    print(effort)
    print(resistance)
    print(pos_mods)
    print(neg_mods)
    if roll <= effort:
        res_num = res_num + 1
        print("Succeeded Effort")
    else:
        res_num = res_num - 1
        print("Failed Effort")
    
    if roll <= resistance:
        res_num = res_num - 1
        print("Beat by Resistance")
    else:
        print("Overcame Resistance")
    
    for mod in pos_mods:
        if roll <= mod:
            res_num = res_num + 1
            print("Succeeded Mod")
    
    for mod in neg_mods:
        if roll <= mod:
            res_num = res_num - 1
            print("Failed Mod")
    
    return res_num
    
def exploration_outcome(result):
    r1 = cost
    r2 = cost
    r3 = cost
    
    if result >= success_crit:
        r1 = reward
        r2 = reward
        r3 = reward
    elif result == success_comp:
        r1 = risk
        r2 = reward
        r3 = reward
    elif result == success_part:
        r2 = risk
        r3 = reward
    elif result == failure_part:
        r2 = risk
        r3 = risk
    elif result == failure_comp:
        r3 = risk
        
    return [r1, r2, r3]
    
def handle_exp_roll(exp):
    roll = get_intput("Exploration Roll: ")
    print(roll)
    result = roll_result(roll, exp.explo, exp.lvl, [exp.perc, exp.eusoc], [])
    
    print_result(result)
    
    return result

hunger_chc = 50
collapse_chc = 45
effects_chc = 30
darkness_chc = 25
renovation_chc = 10

def generate_costs(level):
    roll = get_intput("Enter Roll for Costs:")
    roll = int(roll)
    
    costs = ["Costs"]
    
    if roll <= hunger_chc + level:
        costs.append("Hunger")
    if roll <= collapse_chc + level:
        costs.append("Collapse")
    if roll <= effects_chc + level:
        costs.append("Effects")
    if roll <= darkness_chc + level:
        costs.append("Darkness")
    if roll <= renovation_chc + level:
        costs.append("Renovation")
    
    print("Costs: ", costs)
    
    return costs
    
encounter_chc = 50
item_unk_chc = 40
obstacle_chc = 30
spoilage_chc = 15
infection_chc = 10

def generate_risks(level):
    roll = get_intput("Enter Roll for Risks:")
    roll = int(roll)
    
    risks = ["Risks"]
    
    if roll <= encounter_chc + level:
        risks.append("Encounter")
    if roll <= item_unk_chc + level:
        risks.append("Unknown Item")
    if roll <= obstacle_chc + level:
        risks.append("Obstacle")
    if roll <= spoilage_chc + level:
        risks.append("Spoilage")
    if roll <= infection_chc + level:
        risks.append("Infection")
    
    print("Risks: ", risks)
    
    return risks

room_chc = 100
shortcut_chc = -50
item_knw_chc = 30
resource_chc = 15
level_chc = 10

def generate_rewards(level, perception):
    roll = get_intput("Enter Roll for Rewards:")
    
    roll = int(roll)
    rewards = ["Rewards"]
    
    if roll <= room_chc - level:
        rewards.append("Room")
    if roll <= shortcut_chc + level:
        rewards.append("Shortcut")
    if roll <= item_knw_chc + level:
        rewards.append("Known Item")
    if roll <= resource_chc + level:
        rewards.append("Resource")
    if roll <= level_chc + level:
        rewards.append("Level")
    if roll <= perception - level:
        rewards.append("Secret")
    
    print("Rewards: ", rewards)
    
    return rewards

def generate_events(action, outcome):
    events = []
    
    for o in outcome:
        if o == reward:
            rewards = generate_rewards(action.lvl, action.perc)
            events.append(rewards)
        elif o == risk:
            risks = generate_risks(action.lvl)
            events.append(risks)
        else:
            costs = generate_costs(action.lvl)
            events.append(costs)
    return events

def handle_hunger():
    print("\nHunger\n")
    #3.7.8.1 Hunger
    #2.11.6.7 for consuming food items
    '''
    1. Consumption Roll 2.11.6.6
        Boolean roll. Effort is Item's rating.
        if roll <= Item Rating -> item doesn't change
        elif roll > Item Rating -> 
            if !depleted -> depleted
            elif depleted -> exhausted, delete it.
    2. Roll to reduce Hunger
    '''
    #3.7.8.2 Starvation
    '''
    If you don't spend food ->
        if starving -> dead
        elif hunger >= 100 -> starving
        elif hunger < 100 -> roll to increase
    '''
    
    # New Ideas:
    '''
        Roll with Item Rating as Effort vs Hunger as Resistance
        Boolean Roll. Effort is Item's rating.
        if roll <= Item Rating ->
            Roll to reduce Hunger.
        elif roll > Item Rating ->
            Roll to Increase Hunger.
        Then
            if !depleted -> depleted
            elif depleted -> exhausted, delete it.
    '''
    
    hunger_rating = get_intput("Enter Hunger Rating: ")
    hunger_die = get_quantification_die(hunger_rating)
    food_prompt = input("Use a Food Item? [Y/N] ")
    
    if yes_no(food_prompt):
        food_rating = get_intput("Enter Food Rating: ")
        food_roll = get_intput("Enter Consumption Roll: ")
        if food_roll <= food_rating:
            print("Roll ", hunger_die, " to reduce Hunger.")
        else:
            print("Roll ", hunger_die, " to increase Hunger.")
        
        print("If food item is depleted, remove from inventory.")
        print("If food item is not depleted, mark it depleted.")
    else:
        print("Roll ", hunger_die, " to increase Hunger.")
    
    input("\nHunger Handled. Press Enter to continue...")
    return

def handle_collapse():
    print("\nCollapse\n")
    print("Choose a room to be discarded from the Room Pool.")
    print("Both explored and unexplored rooms can be discarded,")
    print("including the current room.\n")
    print("Room 0 cannot be discarded this way.")
    input("\nCollapse Handled.  Press Enter to continue...")
    return

def handle_effects():
    print("\nEffects\n")
    # Effects 3.7.8.4
    #2.11.5.3 for Checking Effects
    '''
    Single Boolean Roll
    if roll <= Effect -> reduce to 0
    else -> effect triggers
    '''
    #2.11.5.4 - 2.11.5.13 for triggering Effects
    
    input("\nEffects Handled.  Press Enter to continue...")
    return

def handle_darkness(level):
    print("Darkness Handled")
    '''
    Spend a Light Item.
    Make a boolean roll vs Light Rating
    if roll > Light Rating -> Quantify Darkness based on Level
    else -> nothing changes

    Then
        if !depleted -> depleted
        elif depleted -> exhausted, delete it.
    
    '''
    return
    
def handle_renovation():
    print("Choose a random explored room. It is now unexplored.")
    print("The room loses any items or resources that were found there.")
    print("The room otherwise maintains its connections to other rooms.")
    
    input("\nRenovation Handled.  Press Enter to continue...")
    return

def handle_encounter(level):
    # 3.7.9.1 Encounter
    # Encounter Tables
    # Termite: 
    # Bee: (not present)
    # Ant: (not present)
    input("\nEncounter Handled.  Press Enter to continue...")
    return

def handle_item_unknown():
    # Unknown Item 3.7.9.2
    # 2.11.6.8 Generating Food Items
    # 2.11.6.9 Generate Food Item Form
    '''
    1. Color
    2. Food Type
    3. Quantify
    '''
    
    input("\nUnknown Item Handled.  Press Enter to continue...")
    return

def handle_obstacle(level):
    #3.7.9.3 Obstacle
    '''
    1. Quantify Obstacle
    2. Roll Boolean Construction
        if roll <= Construction -> tear down that wall
            Boolean roll vs Obstacle Rating
        else -> take 1 wound
    Players cannot move forward with the current Exploration Action until the obstacle is removed.
    If the players leave the room before clearing the obstacle, they forfeit any remaining risks or rewards.
    '''
    input("\nObstacle Handled.  Press Enter to continue...")
    return

def handle_spoilage():
    input("\nSpoilage Handled.  Press Enter to continue...")
    return

def handle_infection(level):
    '''
    3.7.9.5 Infection
    Boolean vs Level
    if roll <= Level -> 
        if !infected -> Quantify Infection
        else -> Infection Triggers (2.11.5.9)
            If have Effects at 0%:
                Select one of those at random
                Set Effect based on Infected
            Else:
                Choose random Effect (Include Infected)
                Roll to Increase based on Infected
    else -> Nothing. You did it!
    '''
    input("\nInfection Handled.  Press Enter to continue...")
    return

def handle_room(level):
    print("New Room on Level ", level)
    input("\nRoom Handled.  Press Enter to continue...")
    return

def handle_shortcut():
    print("To arms, you ugly bugs!")
    print("You found the Job Target!")
    input("\nShortcut Handled.  Press Enter to continue...")
    return
    
def handle_item_known():
    # Randomly roll among known Items.
    print("Randomly roll among known Items.")
    input("\nKnown Item Handled.  Press Enter to continue...")
    return

def handle_resource(level):
    '''
    If has building -> roll to increase (quantified by level)
    If not has building -> roll to set (quantified by level)
    '''
    resource_die = get_quantification_die(level)
    print("Roll a ", resource_die, " to quantify resource")
    input("\nResource Handled.  Press Enter to continue...")
    return

def handle_level(level):
    # Roll to Increase Level
    print("New Room on Level ")
    input("\nLevel Handled.  Press Enter to continue...")
    return

def handle_secret():
    # 3.7.10.6
    
    # Randomly select Cost, Risk or Rewards
    '''
    Cost:
    1 Hunger
    2 Collapse
    3 Effects
    4 Darkness
    5 Renovation
    '''
    '''
    Risk:
    1 Encounter
    2 Unknown Item
    3 Obstacle 
    4 Spoilage
    5 Infection
    '''
    '''
    Reward:
    1 Room
    2 Shortcut
    3 Known Item
    4 Resource
    5 Level
    6 Secret
    '''
    input("\nSecret Handled.  Press Enter to continue...")
    return
    
def handle_costs(level, costs_list):
    
    for cost in costs_list:
        if cost == "Hunger":
            handle_hunger()
        elif cost == "Collapse":
            handle_collapse()
        elif cost == "Effects":
            handle_effects()
        elif cost == "Darkness":
            handle_darkness(level)
        elif cost == "Renovation":
            handle_renovation()
            
    return

def handle_risks(level, risks_list):
    for risk in risks_list:
        if risk == "Encounter":
            handle_encounter(level)
        elif risk == "Unknown Item":
            handle_item_unknown()
        elif risk == "Obstacle":
            handle_obstacle(level)
        elif risk == "Spoilage":
            handle_spoilage()
        elif risk == "Infection":
            handle_infection(level)
    return
    return

def handle_rewards(level, rewards_list):
     
    for reward in rewards_list:
        if reward == "Room":
            handle_room(level)
        elif reward == "Shortcut":
            handle_shortcut()
        elif reward == "Known Item":
            handle_item_known()
        elif reward == "Resource":
            handle_resource(level)
        elif reward == "Level":
            handle_level()
        elif reward == "Secret":
            handle_secret()
    
    return
    
def handle_events(level, event_lists):
    for event_list in event_lists:
        if event_list[0] == "Rewards":
            handle_rewards(level, event_list)
        elif event_list[0] == "Risks":
            handle_risks(level, event_list)
        elif event_list[0] == "Costs":
            handle_costs(level, event_list)
        

def exploration_action(exp_act):
    
    exp_res = handle_exp_roll(exp_act)
    
    exp_out = exploration_outcome(exp_res)
    
    events = generate_events(exp_act,exp_out)
    
    handle_events(exp_act.lvl, events)
    
exp_action = get_information()
is_done = 0
do_change = False

while not yes_no(is_done):
    if do_change:
        exp_action = get_information()
    
    exploration_action(exp_action)
    
    is_done = input("Is done? [Y/N] ")
    if not yes_no(is_done):
        do_change = is_change()