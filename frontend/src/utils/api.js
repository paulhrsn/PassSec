//api.js
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5001/api";



// helper that automatically sends your login info with every request
// and logs you out if the server says you’re not authorized
async function authFetch(url, options = {}) {
  const token = localStorage.getItem("token"); //gets saved login token from local storage
  const headers = { ...(options.headers || {}) }; //use provided headers
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(url, { ...options, headers });


  if (res.status === 401 || res.status === 422) {
    // nuke stale state so navbar stops showing "logged in"
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
  }

  return res;
}
  
//  @param {{ email: string, password: string }}
// @returns {Promise<{ token: string, user: object } | { error: string }>}
 
export async function loginUser({ email, password }) {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.trim(), password }),
    });

    const data = await res.json();

    if (!res.ok) {
      return { error: data.message || "Login failed" };
    }

    return { token: data.token, user: data.user };
  } catch (err) {
    console.error("loginUser network error:", err);
    return { error: "Network error" };
  }
}

 // @param {{ email: string, password: string }}
 // @returns {Promise<{ error: string }>}
 
 export async function registerUser({ email, password }) {
  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.trim(), password }),
    });

    const data = await res.json();

    if (!res.ok) {
      return { error: data.error || data.message || "Registration failed" };
    }

    return {}; //success
  } catch (err) {
    console.error("registerUser network error:", err);
    return { error: "Network error" };
  }
}




  
  //@param {{ domain?: string, count?: number }}
  //@returns {Promise<Array>} Array of quiz questions
 
export async function fetchQuizQuestions({ domain = "", count = 5 }) {
  const url = new URL(`${API_BASE}/quiz`);
  if (domain) url.searchParams.append("domain", domain);
  if (count)  url.searchParams.append("count", count);

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch quiz questions");

  return res.json();
}

  
  //@param {{ answers: Array<{ question_id: number, answer: string }> }}
  //@returns {Promise<{ score: number, total: number }>}
 
  export async function submitQuizAnswers({ answers, domain }) {
    const res = await authFetch(`${API_BASE}/quiz/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers, domain })
    });
    if (!res.ok) throw new Error("Quiz submission failed");
    return res.json();
  }
  



 
 //@returns {Promise<Array>} List of lab summaries
 
export async function fetchAllLabs() {
  const res = await fetch(`${API_BASE}/labs`);
  if (!res.ok) throw new Error("Failed to fetch labs");
  return res.json();
}

 //@param {string|number} labId
 //@returns {Promise<object>} Lab data
 
export async function fetchLab(labId) {
  const res = await fetch(`${API_BASE}/labs/${labId}`);
  if (!res.ok) throw new Error(`Failed to fetch lab (${res.status})`);
  return res.json();
}

  
//  @param {{ userId: string, labId: string, answer: string }}
 // @returns {Promise<object>} Result (e.g. correct/incorrect)

 export async function submitLabAnswer(data) {
  const res = await authFetch(`${API_BASE}/labs/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Submission failed");
  return res.json();
}



export async function fetchUserStats() {
  const res = await authFetch(`${API_BASE}/dashboard/stats`);
  if (res.status === 401 || res.status === 422) throw new Error("Unauthorized");
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}

 
 // @returns {Promise<{ status: string }>}
 
export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
