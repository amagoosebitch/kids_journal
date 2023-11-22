export const AppRoute = {
  Main: "/",
  SignIn: "/login",
  Error: "/*",
};

export enum AuthorizationStatus {
  Auth = "AUTH",
  NoAuth = "NO_AUTH",
  Unknown = "UNKNOWN",
}
