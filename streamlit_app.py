import json
import requests
import streamlit as st

# URL of the MLflow prediction server
url = "http://127.0.0.1:8000/invocations"  # Modify if needed, based on your setup

# Preload sample input data
@st.cache_data
def get_sample_input():
    return {
        "Order": 1,
        "PID": 5286,
        "MS SubClass": 20,
        "Lot Frontage": 80.0,
        "Lot Area": 9600,
        "Overall Qual": 5,
        "Overall Cond": 7,
        "Year Built": 1961,
        "Year Remod/Add": 1961,
        "Mas Vnr Area": 0.0,
        "BsmtFin SF 1": 700.0,
        "BsmtFin SF 2": 0.0,
        "Bsmt Unf SF": 150.0,
        "Total Bsmt SF": 850.0,
        "1st Flr SF": 856,
        "2nd Flr SF": 854,
        "Low Qual Fin SF": 0,
        "Gr Liv Area": 1710.0,
        "Bsmt Full Bath": 1,
        "Bsmt Half Bath": 0,
        "Full Bath": 1,
        "Half Bath": 0,
        "Bedroom AbvGr": 3,
        "Kitchen AbvGr": 1,
        "TotRms AbvGrd": 7,
        "Fireplaces": 2,
        "Garage Yr Blt": 1961,
        "Garage Cars": 2,
        "Garage Area": 500.0,
        "Wood Deck SF": 210.0,
        "Open Porch SF": 0,
        "Enclosed Porch": 0,
        "3Ssn Porch": 0,
        "Screen Porch": 0,
        "Pool Area": 0,
        "Misc Val": 0,
        "Mo Sold": 5,
        "Yr Sold": 2010,
    }

# Main function for Streamlit app
def main():
    st.title("End-to-End House Price Prediction Project")

    # Load sample input data
    sample_input = get_sample_input()

    # Sidebar inputs for model features with preloaded sample data
    order = st.sidebar.number_input("Order", value=sample_input["Order"])
    pid = st.sidebar.number_input("PID", value=sample_input["PID"])
    ms_subclass = st.sidebar.slider("MS SubClass", min_value=0, max_value=200, value=sample_input["MS SubClass"])
    lot_frontage = st.sidebar.number_input("Lot Frontage", value=sample_input["Lot Frontage"])
    lot_area = st.sidebar.number_input("Lot Area", value=sample_input["Lot Area"])
    overall_qual = st.sidebar.slider("Overall Quality", min_value=1, max_value=10, value=sample_input["Overall Qual"])
    overall_cond = st.sidebar.slider("Overall Condition", min_value=1, max_value=10, value=sample_input["Overall Cond"])
    year_built = st.sidebar.number_input("Year Built", value=sample_input["Year Built"])
    year_remod_add = st.sidebar.number_input("Year Remodeled/Added", value=sample_input["Year Remod/Add"])
    mas_vnr_area = st.sidebar.number_input("Masonry Veneer Area", value=sample_input["Mas Vnr Area"])
    bsmtfin_sf1 = st.sidebar.number_input("Basement Finished SF 1", value=sample_input["BsmtFin SF 1"])
    bsmtfin_sf2 = st.sidebar.number_input("Basement Finished SF 2", value=sample_input["BsmtFin SF 2"])
    bsmt_unf_sf = st.sidebar.number_input("Basement Unfinished SF", value=sample_input["Bsmt Unf SF"])
    total_bsmt_sf = st.sidebar.number_input("Total Basement SF", value=sample_input["Total Bsmt SF"])
    first_flr_sf = st.sidebar.number_input("1st Floor SF", value=sample_input["1st Flr SF"])
    second_flr_sf = st.sidebar.number_input("2nd Floor SF", value=sample_input["2nd Flr SF"])
    low_qual_fin_sf = st.sidebar.number_input("Low Quality Finished SF", value=sample_input["Low Qual Fin SF"])
    gr_liv_area = st.sidebar.number_input("Ground Living Area SF", value=sample_input["Gr Liv Area"])
    bsmt_full_bath = st.sidebar.slider("Basement Full Baths", min_value=0, max_value=5, value=sample_input["Bsmt Full Bath"])
    bsmt_half_bath = st.sidebar.slider("Basement Half Baths", min_value=0, max_value=5, value=sample_input["Bsmt Half Bath"])
    full_bath = st.sidebar.slider("Full Baths", min_value=0, max_value=5, value=sample_input["Full Bath"])
    half_bath = st.sidebar.slider("Half Baths", min_value=0, max_value=5, value=sample_input["Half Bath"])
    bedroom_abvgr = st.sidebar.slider("Bedrooms Above Ground", min_value=0, max_value=10, value=sample_input["Bedroom AbvGr"])
    kitchen_abvgr = st.sidebar.slider("Kitchens Above Ground", min_value=0, max_value=5, value=sample_input["Kitchen AbvGr"])
    totrms_abvgrd = st.sidebar.slider("Total Rooms Above Ground", min_value=0, max_value=20, value=sample_input["TotRms AbvGrd"])
    fireplaces = st.sidebar.slider("Fireplaces", min_value=0, max_value=5, value=sample_input["Fireplaces"])
    garage_yr_blt = st.sidebar.number_input("Garage Year Built", value=sample_input["Garage Yr Blt"])
    garage_cars = st.sidebar.slider("Garage Cars", min_value=0, max_value=5, value=sample_input["Garage Cars"])
    garage_area = st.sidebar.number_input("Garage Area", value=sample_input["Garage Area"])
    wood_deck_sf = st.sidebar.number_input("Wood Deck SF", value=sample_input["Wood Deck SF"])
    open_porch_sf = st.sidebar.number_input("Open Porch SF", value=sample_input["Open Porch SF"])
    enclosed_porch = st.sidebar.number_input("Enclosed Porch", value=sample_input["Enclosed Porch"])
    three_ssn_porch = st.sidebar.number_input("3 Season Porch", value=sample_input["3Ssn Porch"])
    screen_porch = st.sidebar.number_input("Screen Porch", value=sample_input["Screen Porch"])
    pool_area = st.sidebar.number_input("Pool Area", value=sample_input["Pool Area"])
    misc_val = st.sidebar.number_input("Miscellaneous Value", value=sample_input["Misc Val"])
    mo_sold = st.sidebar.slider("Month Sold", min_value=1, max_value=12, value=sample_input["Mo Sold"])
    yr_sold = st.sidebar.number_input("Year Sold", value=sample_input["Yr Sold"])

    # Button for prediction
    if st.button("Predict"):
        # Prepare the user input (same as sample_input but can be modified by the user)
        user_input = {
            "Order": order,
            "PID": pid,
            "MS SubClass": ms_subclass,
            "Lot Frontage": lot_frontage,
            "Lot Area": lot_area,
            "Overall Qual": overall_qual,
            "Overall Cond": overall_cond,
            "Year Built": year_built,
            "Year Remod/Add": year_remod_add,
            "Mas Vnr Area": mas_vnr_area,
            "BsmtFin SF 1": bsmtfin_sf1,
            "BsmtFin SF 2": bsmtfin_sf2,
            "Bsmt Unf SF": bsmt_unf_sf,
            "Total Bsmt SF": total_bsmt_sf,
            "1st Flr SF": first_flr_sf,
            "2nd Flr SF": second_flr_sf,
            "Low Qual Fin SF": low_qual_fin_sf,
            "Gr Liv Area": gr_liv_area,
            "Bsmt Full Bath": bsmt_full_bath,
            "Bsmt Half Bath": bsmt_half_bath,
            "Full Bath": full_bath,
            "Half Bath": half_bath,
            "Bedroom AbvGr": bedroom_abvgr,
            "Kitchen AbvGr": kitchen_abvgr,
            "TotRms AbvGrd": totrms_abvgrd,
            "Fireplaces": fireplaces,
            "Garage Yr Blt": garage_yr_blt,
            "Garage Cars": garage_cars,
            "Garage Area": garage_area,
            "Wood Deck SF": wood_deck_sf,
            "Open Porch SF": open_porch_sf,
            "Enclosed Porch": enclosed_porch,
            "3Ssn Porch": three_ssn_porch,
            "Screen Porch": screen_porch,
            "Pool Area": pool_area,
            "Misc Val": misc_val,
            "Mo Sold": mo_sold,
            "Yr Sold": yr_sold,
        }

        # Prepare the request payload as 'instances'
        payload = {"instances": [user_input]}

        # Make the prediction request to the MLflow model
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            # Get the prediction result from the JSON response
            prediction = response.json().get('predictions', None)
    
            if prediction is not None:
                # Display the prediction result
                st.write(f"Predicted Price: {prediction[0]}")
            else:
                st.error("Prediction result not found in the response.")
        else:
            st.error(f"Prediction failed. Error: {response.text}")

if __name__ == "__main__":
    main()
