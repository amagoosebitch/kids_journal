import React, { DOMAttributes } from "react";
import "./MenuButton.css";

export interface MenuButtonProps extends DOMAttributes<HTMLButtonElement> {
  isActive: boolean;
  onClick: (event: React.MouseEvent) => void;
}

export const MenuButton = ({ isActive, onClick }: MenuButtonProps) => {
  return (
    <button
      onClick={onClick}
      className={`header__menu-button
        ${isActive ? "active" : "inactive"}`}
    >
      <span></span>
    </button>
  );
};
