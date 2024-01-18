import React, {useEffect, useState} from "react";
import {useNavigate, useSearchParams} from "react-router-dom";
import Cookies from "js-cookie";
import {jwtDecode} from "jwt-decode";
import {ApiRoute, AppRoute} from "./const";
import {cookieType} from "./pages/welcome-screen/welcome-screen";
import {NavigateFunction} from "react-router/dist/lib/hooks";

export function AuthMiddleware (navigate: NavigateFunction) {
      let decoded = cookieType
      let phone_number = '';
      const cookie = Cookies.get('Authorization')
      if (cookie) {
        decoded = jwtDecode(cookie)
        phone_number = decoded.phone_number;
        return phone_number;
      }
      navigate(`${AppRoute.SignIn}`);
}