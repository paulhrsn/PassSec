//environment var setup for defining backend url in .env file
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";
//^ defaults to localhost if nothing's set

//login function, sends post request to my flask /api/login route
//accepts { email, password }
//returns  { token, user } on success or { error } on failure

export async function loginUser(credentials) {
    try {
        const res = await fetch('${API_URL}/login', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(credentials) //convert js input object to json string
        });
        return await res.json() //parse json response
    } catch (err) {
        console.error("Login failed:", err);
        return { error: "Network error" };
    }
}
