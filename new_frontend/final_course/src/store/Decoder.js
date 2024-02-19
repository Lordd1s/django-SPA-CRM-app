import { jwtDecode, InvalidTokenError } from "jwt-decode";

export function parseJwt(token) {
    try {
      const decoded = jwtDecode(token);
      // console.log(decoded);
      return decoded;
    } catch (error) {
      console.log("Error decoding JWT:", error);
      return null;
    }
  }