import React, { useState, useRef, useEffect } from "react";
import { useClickOutside } from "../../hooks/useClickOutside";
import { BsFillPersonFill, BsBoxArrowRight } from "react-icons/bs";
import { Avatar } from "@chakra-ui/react";
import "./MenuList.css";

export type MenuListOption = {
  label: string;
  value: string | number;
};

type MenuListProps = {
  value?: MenuListOption;
  onChange: (value: MenuListOption | undefined) => void;
};

type MenuProps = {
  options: MenuListOption[];
} & MenuListProps;

export const MenuList = ({ value, onChange, options }: MenuProps) => {
  const [isOpen, setOpen] = useState(false);
  const menuRef = useRef(null);
  useClickOutside(menuRef, () => {
    if (isOpen) setTimeout(() => setOpen(false), 50);
  });

  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  function clearOptions() {
    onChange(undefined);
  }

  function MenuListOption(option: MenuListOption) {
    if (option !== value) onChange(option);
  }

  function isOptionSelected(option: MenuListOption) {
    return option === value;
  }

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target != containerRef.current) return;
      switch (e.code) {
        case "Enter":
        case "Space":
          setOpen((prev) => !prev);
          if (isOpen) MenuListOption(options[highlightedIndex]);
          break;
        case "ArrowUp":
        case "ArrowDown": {
          if (!isOpen) {
            setOpen(true);
            break;
          }

          const newValue = highlightedIndex + (e.code === "ArrowDown" ? 1 : -1);
          if (newValue >= 0 && newValue < options.length) {
            setHighlightedIndex(newValue);
          }
          break;
        }
        case "Escape":
          setOpen(false);
          break;
      }
    };
    containerRef.current?.addEventListener("keydown", handler);

    return () => {
      containerRef.current?.removeEventListener("keydown", handler);
    };
  }, [isOpen, highlightedIndex, options]);

  return (
    <>
      <button className="menu-button" onClick={() => setOpen(!isOpen)}>
        <Avatar size="lg" />
      </button>
      <nav className={`menu ${isOpen ? "active" : ""}`}>
        <ul className="menu__list">
          {options.map((option, index) => (
            <li
              onClick={(e) => {
                e.stopPropagation();
                MenuListOption(option);
                setOpen(false);
              }}
              onMouseEnter={() => setHighlightedIndex(index)}
              key={option.value}
              className={`optionMenu ${
                isOptionSelected(option) ? "selectedMenu" : ""
              } ${index === highlightedIndex ? "highlightedMenu" : ""}`}
            >
              {option.label}
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
};
