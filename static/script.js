document.getElementById('predictionForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = {};

    formData.forEach((value, key) => {
        // Convert numeric fields to float
        if (["MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm", "Temp9am", "Temp3pm"].includes(key)) {
            data[key] = parseFloat(value);
        } else if (["Cloud9am", "Cloud3pm", "RainToday"].includes(key)) {
            data[key] = isNaN(parseInt(value)) ? value : parseInt(value);
        } else {
            data[key] = value; // Keep as string
        }
    });

    console.log("Processed Data:", data);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        console.log("Backend response:", result);

        document.getElementById('result').innerHTML = `
            <h3>Prediction: ${result['Rainfall Prediction']}</h3>
            <p>Probability: ${result['Probability']}</p>
        `;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById('result').innerHTML = `<p>Something went wrong. Please try again later.</p>`;
    }
});
