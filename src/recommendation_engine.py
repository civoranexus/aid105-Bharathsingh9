import pandas as pd

# Load datasets
users = pd.read_csv("data/users.csv")
schemes = pd.read_csv("data/schemes.csv")

# 🔥 FORCE CLEAN income_limit column
schemes["income_limit"] = (
    schemes["income_limit"]
    .astype(str)                 # ensure string
    .str.replace(",", "")        # remove commas if any
)

schemes["income_limit"] = pd.to_numeric(
    schemes["income_limit"], errors="coerce"
)

# DEBUG: confirm conversion
print("Income limit dtype AFTER fix:", schemes["income_limit"].dtype)
print(schemes["income_limit"].head())

def is_eligible(user, scheme):
    # Age check
    if not (int(scheme["min_age"]) <= int(user["age"]) <= int(scheme["max_age"])):
        return False

    # Income check (ONLY if limit exists)
    if pd.notna(scheme["income_limit"]):
        if int(user["annual_income"]) > int(scheme["income_limit"]):
            return False

    # State check
    if scheme["state"] != "All" and user["state"] != scheme["state"]:
        return False

    # Category check
    if scheme["category"] != "All" and user["category"] not in scheme["category"]:
        return False

    # Gender check
    if scheme["gender"] != "All" and user["gender"] != scheme["gender"]:
        return False

    return True


if __name__ == "__main__":
    user = users.iloc[0]
    scheme = schemes.iloc[0]

    print("\nTesting eligibility:")
    print("User income:", user["annual_income"])
    print("Scheme income limit:", scheme["income_limit"])

    result = is_eligible(user, scheme)
    print("Is user eligible?", result)
