//base url for API calls, pulls from vite env var (VITE_API_URL) or falls back to local dev if that fails
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

//loginUser to hit /api/login endpoint:
//accepts object { email, password }
//on success, returns { token, user }
//on HTTP error will return { error : "..." }
//on network error returns { error : "Network error" }
export async function loginUser({ email, password}) {
    try {
        const res = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            //converts js object to json string for http body
            body: JSON.stringify({ email: email.trim(), password }),
        });

        //parse json response
        const data = await res.json();

        //if http status not in 200-299 range then it's an error
        if (!res.ok) {
            return { error: data.message || "Login Failed"};
        }

        //on success return the jwt token and other user backend objects
        return { token: data.token, user:data.user };
    } catch (err) {
        //network failure like DNS lands here i think
        console.error("loginUser network error:", err);
        return { error: "Network error" };
    }
}

//placeholder stubs for my endpoints later
//i think they can all be the same structure as above

export async function registerUser({ email, password }) {
    // same structure, POST to `${API_BASE_URL}/register`
    return { error: "registerUser not implemented" };
  }
  
  export async function fetchQuizQuestions() {
    //  GET `${API_BASE_URL}/quiz`
    return { error: "registerUser not implemented" };
  }
  
  export async function submitQuizAnswers(answers) {
    //  POST `${API_BASE_URL}/quiz/submit`
    return { error: "registerUser not implemented" };
  }

  export async function checkHealth() {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/health`);
    const data = await res.json();
    return data;
  }
  