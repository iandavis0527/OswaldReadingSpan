import Cookies from "js-cookie";


export function isUserLoggedIn(): boolean {
    return Cookies.get("authenticated") === "true";
}

export async function login(username: string, password: string): Promise<boolean> {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const result = await fetch("login", {
        body: formData,
    });

    if (result.status === 200) Cookies.set("authenticated", "true");

    return result.status === 200;
}
