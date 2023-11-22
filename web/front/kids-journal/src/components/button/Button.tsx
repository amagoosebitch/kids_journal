import React, { DOMAttributes } from "react";
import classNames from "classnames";
import "./Button.css";

export type ButtonType = "button" | "submit" | "reset";

export interface ButtonProps extends DOMAttributes<HTMLButtonElement> {
  className?: string;
  isDisable?: boolean;
  typeButton?: ButtonType;
  onClick?: (event: React.MouseEvent) => void;
}

export const Button: React.FC<ButtonProps> = ({
  className,
  children,
  isDisable,
  typeButton,
  onClick,
  ...props
}) => {
  return (
    <button
      className={classNames("Button", className, {
        Button__disabled: isDisable,
      })}
      disabled={isDisable}
      type={typeButton}
      onClick={onClick}
      {...props}
    >
      <span>{children}</span>
    </button>
  );
};
