import json
import streamlit as st
from streamlit_javascript import st_javascript

def main():
    st.title("Field Data Collection App")

    # Initial state for location check
    if "location_enabled" not in st.session_state:
        st.session_state.location_enabled = False

    # Step 1: Ask the user to enable location
    if not st.session_state.location_enabled:
        st.warning("Please enable your location to proceed.")
        if st.button("I have enabled my location"):
            st.session_state.location_enabled = True
        return  # Exit early until location is enabled

    # Step 2: Use JavaScript to capture user coordinates
    coords_raw = st_javascript("""
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve(JSON.stringify({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    }));
                },
                (error) => {
                    resolve(JSON.stringify({ error: error.message }));
                }
            );
        });
    """)

    # Debugging: Show raw JavaScript output
    st.write(f"Raw JS Output: {coords_raw}")

    # Parse the JavaScript result
    if isinstance(coords_raw, str):
        try:
            coords = json.loads(coords_raw)
        except json.JSONDecodeError:
            coords = {"error": "Failed to decode JSON"}
    else:
        coords = {"error": f"Unexpected return type: {type(coords_raw).__name__}"}

    # Step 3: Display coordinates or error message
    if "latitude" in coords and "longitude" in coords:
        st.success(f"Coordinates Captured: {coords['latitude']}, {coords['longitude']}")
    elif "error" in coords:
        st.error(f"Failed to capture coordinates: {coords['error']}")
    else:
        st.error("Unable to retrieve coordinates. Ensure location permissions are enabled.")

    # Step 4: Display a form for data collection
    with st.form("field_form"):
        st.subheader("Field Data Form")
        q1 = st.text_input("Question 1: What is your name?")
        q2 = st.text_input("Question 2: What is your role?")
        q3 = st.text_area("Question 3: Describe your task today.")
        q4 = st.text_input("Question 4: Any additional notes?")

        # Display captured coordinates in disabled fields
        latitude = st.text_input("Latitude (Auto-captured)", coords.get("latitude", ""), disabled=True)
        longitude = st.text_input("Longitude (Auto-captured)", coords.get("longitude", ""), disabled=True)

        # Submit button
        submitted = st.form_submit_button("Submit")

        # Handle form submission
        if submitted:
            if "latitude" in coords and "longitude" in coords:
                st.success("Form submitted successfully!")
                st.write("**Captured Data:**")
                st.write({
                    "Name": q1,
                    "Role": q2,
                    "Task": q3,
                    "Notes": q4,
                    "Latitude": latitude,
                    "Longitude": longitude,
                })
            else:
                st.warning("Coordinates not captured. Ensure location permissions are enabled and try again.")

if __name__ == "__main__":
    main()