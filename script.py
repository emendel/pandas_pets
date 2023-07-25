import pandas as pd
owners = pd.read_csv('owners.csv')
pets = pd.read_csv('pets.csv')
procedure_details = pd.read_csv('procedure_details.csv')
procedures = pd.read_csv('procedures.csv')

def pets_per_city():
    num_cities = owners['City'].value_counts().size
    num_pets = pets.shape[0]
    return num_pets/num_cities


def oldest_dog(city):
    df = pd.merge(pets, owners, on='OwnerID')
    animals = df.loc[df['City'] == city]
    dogs = animals.loc[animals["Kind"] == "Dog"].sort_values(by="Age", ascending=False).head(1)
    return dogs["Name_x"].values[0]




#Which owner spent the most on procedures 
#for their pet(s)?
def max_procedure_costs_and_cost_over_20():
    cost = {}
    pets_owners = pd.merge(pets, owners, on='OwnerID')
    df = pd.merge(pets_owners, procedures, on='PetID')
    for index, row in df.iterrows():
        p_type = row["ProcedureType"]
        p_subcode = row["ProcedureSubCode"]
        owner = row["OwnerID"]
        price = procedure_details.loc[(procedure_details['ProcedureType'] == p_type) 
                              & (procedure_details['ProcedureSubCode'] == p_subcode), 'Price']
        price = price.values[0]
        if owner not in cost:
            cost[owner] = price
        else:
            cost[owner] += price




    max_owner_id = ""
    max_owner_cost = 0

    owners_over_twenry = 0
    for x in cost:
        if cost[x] >= 20:
            owners_over_twenry += 1
        if max_owner_cost < cost[x]:
            max_owner_id = x
            max_owner_cost = cost[x]
    owner_name = owners.loc[owners['OwnerID'] == max_owner_id].Name

    print("Which owner spent most of procedures? ", owner_name.values[0])
    print("How many owners spent 20 dollars or more on procedures for their pets?  ", owners_over_twenry)



#How many owners have at least 
# two different kinds of pets (e.g. a dog and a cat)?
def two_pets():
    df = pd.merge(pets, owners, on='OwnerID')
    groups = df.groupby('OwnerID')
    unique_values = groups['Kind'].unique()
    count = 0
    for x in unique_values:
        if x.shape[0] > 1:
            count +=1 
    return count





#How many owners have pets where 
# the first letter of their name 
# (OwnerName) matches the first letter 
# of their pet's name (PetName)? 
# E.g. Cookie and Charles.
def same_name():
    df = pd.merge(pets, owners, on='OwnerID')
    # groupby two columns
    df = df.groupby(['Name_y', 'Name_x'])
    count = 0
    for x in df:
        if x[0][0][0] == x[0][1][0]:
            count += 1
    return(count)



#What percentage of pets received a vaccination?
def vax():
    num_pets = pets.shape[0]
    df = pd.merge(pets, procedures, on='PetID')
    df = df[df.ProcedureType == "VACCINATIONS"]
    unique_values = df.PetID.unique().size
    return(unique_values)



# What percentage of cities have 
# more male pets than female pets?
def male_cities():
    pets_with_cities = pd.merge(pets, owners, on='OwnerID')
    groups = pets_with_cities.groupby('City')
    count = 0

    for name, group in groups:
        males = len(group.loc[group['Gender'] == "male"])
        females = len(group.loc[group['Gender'] == "female"])
        if (males > females):
            count +=1 
    return count/len(groups)



# Which city's pet sample is made 
# up of exactly 70% dogs? The answer 
# is case sensitive, so please match 
# the value for City exactly.
def seventy_percent():
    pets_with_cities = pd.merge(pets, owners, on='OwnerID')
    groups = pets_with_cities.groupby('City')

    # print the groups
    for name, group in groups:
        dogs = len(group.loc[group['Kind'] == "Dog"])
        if dogs/len(group) == 0.7:
            return(name)

print("number of pets per city: ", pets_per_city())
print("oldest dog in southfield: ", oldest_dog("Southfield"))
max_procedure_costs_and_cost_over_20()
print("How many owners have multiple kinds of pets? ", two_pets())
print("How many owners have the same first letter as their pet? ", same_name())
print("What percentage of pets received a vaccination? ", vax())
print("What percentage of cities have more male than female pets? ", male_cities())
print("Which city is 70 percent dogs? ", seventy_percent())
