import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Avatar } from "@chakra-ui/react";
import { SingleValue } from "react-select";

import { useClickOutside } from "../../hooks/useClickOutside";
import { MenuButton } from "../menuButton/MenuButton";
import "../menuButton/MenuButton.css";
import "../menuList/MenuList.css";
import "./Header.css";

import { AppRoute, ApiRoute, infoOrganization } from "../../const";
import { Select, SelectOption } from "../singleSelect/SingleSelect";
import Cookies from 'js-cookie';
import { jwtDecode } from "jwt-decode";

const optionsMenu = [
  { label: "Выйти", value: 2, link: AppRoute.WelcomeScreen },
];

export type MenuListOption = {
  label: string;
  value: string | number;
};

export const organizationInfo = [""];

export const Header = () => {
  const { organization } = useParams();

  const [valueMenu, setValueMenu] = useState<MenuListOption | undefined>(
    optionsMenu[0],
  );
  function MenuListOption(option: MenuListOption) {
    if (option !== valueMenu) setValueMenu(option);
  }

  const [highlightedIndexMenu, setHighlightedIndexMenu] = useState(0);

  function isOptionMenu(option: MenuListOption) {
    return option === valueMenu;
  }

  const options = infoOrganization.map((group, index: number | string) => ({
    label: group.name,
    value: index,
  }));

  const [value, setValue] = useState(
    options.find((obj) => obj.label === organization),
  );

  const navigate = useNavigate();

  const changeSelect = (event: SelectOption) => {
    event
      ? setValue({ label: event.label, value: event.value })
      : setValue(options.find((obj) => obj.label === organization));

    navigate(`/${value?.label}/main`);
  };

  const [isOpenMenu, setOpenMenu] = useState(false);

  const [isOpen, setOpen] = useState(false);
  const closeMobileMenu = () => setOpen(false);
  const menuRef = useRef(null);
  useClickOutside(menuRef, () => {
    if (isOpen) setTimeout(closeMobileMenu, 50);
  });

  useEffect(() => {
    let startTouchX = 0;
    let endTouchX = 0;
    let startTouchY = 0;
    let endTouchY = 0;

    document.addEventListener("touchstart", (event) => {
      startTouchX = event.changedTouches[0].pageX;
      startTouchY = event.changedTouches[0].pageY;
    });

    document.addEventListener("touchend", (event) => {
      endTouchX = event.changedTouches[0].pageX;
      endTouchY = event.changedTouches[0].pageY;
      if (
        startTouchX < 300 &&
        Math.abs(endTouchY - startTouchY) < 40 &&
        endTouchX > startTouchX
      )
        setOpen(true);
      if (
        startTouchX < 900 &&
        Math.abs(endTouchY - startTouchY) < 40 &&
        endTouchX < startTouchX
      )
        setOpen(false);
    });
  }, []);

  return (
    <header className="header">
      <Link
        to={`/${organization}/main`}
        className="header__logo"
        onClick={closeMobileMenu}
      >
        Kids Journal
      </Link>

      <div className="organization">
        <Select
          options={options}
          value={value}
          onChange={(e: SelectOption) => changeSelect(e)}
        />
      </div>

      <nav className={`header__nav ${isOpen ? "active" : ""}`} ref={menuRef}>
        <ul className="header__nav-list">
          <li className="header__nav-item">
            <Link
              to={`/${value?.label}/groups`}
              className="nav-links"
              onClick={closeMobileMenu}
            >
              Группы
            </Link>
          </li>
          <li className="header__nav-item">
            <Link
              to={`/${value?.label}/employees`}
              className="nav-links"
              onClick={closeMobileMenu}
            >
              Сотрудники
            </Link>
          </li>
          <li className="header__nav-item">
            <Link
              to={`/${value?.label}/activity`}
              className="nav-links"
              onClick={closeMobileMenu}
            >
              Активности
            </Link>
          </li>
          <li className="header__nav-item">
            <button
              className="menu-button"
              onClick={() => setOpenMenu(!isOpenMenu)}
            >
              <Avatar size="lg" />
            </button>

            <nav className={`menu ${isOpenMenu ? "active" : ""}`}>
              <ul className="menu__list">
                {optionsMenu.map((option, index) => (
                  <Link to={option.link}>
                    <li
                      onClick={(e) => {
                        e.stopPropagation();
                        MenuListOption(option);
                        setOpenMenu(false);
                        if (option.label == "Выйти") {
                          Cookies.remove("Authorization");
                        }
                      }}
                      onMouseEnter={() => setHighlightedIndexMenu(index)}
                      key={option.value}
                      className={`menu__item optionMenu ${
                        isOptionMenu(option) ? "selectedMenu" : ""
                      } ${
                        index === highlightedIndexMenu ? "highlightedMenu" : ""
                      }`}
                    >
                      {option.label}
                    </li>
                  </Link>
                ))}
              </ul>
            </nav>
          </li>
        </ul>
      </nav>
      <MenuButton isActive={isOpen} onClick={() => setOpen(!isOpen)} />
    </header>
  );
};
