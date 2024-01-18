import React, { DOMAttributes } from "react";
import classNames from "classnames";
import "./ButtonHead.css";
import { Link } from "react-router-dom";
import { AppRoute } from "../../const";

export type ButtonType = "button" | "submit" | "reset";
export const Styles = ["btn--primary", "btn--outline"];
export const Size = ["btn--medium", "btn--large"];

export interface ButtonHeaderProps extends DOMAttributes<HTMLButtonElement> {
  children?: string;
  type?: ButtonType;
  onClick?: (event: React.MouseEvent) => void;
  buttonStyle: string;
  buttonSize: string;
}

export const ButtonHeader = ({
  children,
  type,
  onClick,
  buttonStyle,
  buttonSize,
}: ButtonHeaderProps) => {
  const checkButtonStyle = Styles.includes(buttonStyle)
    ? buttonStyle
    : Styles[0];

  const checkButtonSize = Size.includes(buttonSize) ? buttonSize : Size[0];

  return (
    <Link to={AppRoute.SignUp} className="btn-mobile">
      <button
        className={`btn ${checkButtonStyle} ${checkButtonSize}`}
        onClick={onClick}
        type={type}
      >
        {children}
      </button>
    </Link>
  );
};
