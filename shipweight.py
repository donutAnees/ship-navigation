def check_route_feasibility(ship_base_weight, goods_weight, routes, base_draft):
    """
    Check route feasibilitty based on the ships draft wrt the goods.

    Parameters:
    ship_base_weight: The base weight of the ship in tons(intitially empty without goods)
    goods_weight: The total weight of the goods loaded.
    routes: It contains a list of routes that includes name, distance, and max draft.
    base_draft: Base draft of the ship in meters at base weight.

    Returns:
    - list: A summary of route feasibility (Feasible or Not Feasible) for each route.
    """
    draft_increase_per_ton = 0.002 #random value for each load increase 
    total_weight =ship_base_weight + goods_weight #full weight of the ship
    adjusted_draft =base_draft + ((total_weight - ship_base_weight) * draft_increase_per_ton) #calculating the draft with goods loaded
    route_options = []

    for route in routes:
        max_draft = route['max_draft'] #maxdraft is the maximum draft allowed in that particular route
        route_name = route['name']
        if adjusted_draft > max_draft:
            feasibility = "Not Feasible"
        else:
            feasibility = "Feasible"
        route_options.append({
            "Route": route_name,
            "Feasibility": feasibility
        })
    
    return route_options


