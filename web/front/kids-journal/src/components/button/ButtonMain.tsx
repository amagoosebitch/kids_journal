import React, { DOMAttributes } from "react";
import classNames from "classnames";
import "./Button.css";
import { Link } from "react-router-dom";

export type ButtonType = "button" | "submit" | "reset";

export interface ButtonProps extends DOMAttributes<HTMLButtonElement> {
  className?: string;
  isDisable?: boolean;
  typeButton?: ButtonType;
  onClick?: (event: React.MouseEvent) => void;
  background?: string;
  height: string;
  width: string;
  linkButton: string;
}

export const ButtonMain: React.FC<ButtonProps> = ({
  className,
  children,
  isDisable,
  typeButton,
  onClick,
  height,
  width,
  linkButton,
  background,
  ...props
}) => {
  return (
    <Link to={linkButton}>
      <button
        className={classNames("button", className, {
          Button__disabled: isDisable,
        })}
        disabled={isDisable}
        type={typeButton}
        onClick={onClick}
        style={{
          height: `${height}`,
          width: `${width}`,
          background: `${background}`,
        }}
        {...props}
      >
        <span className="button_children">{children}</span>
      </button>
    </Link>
  );
};
