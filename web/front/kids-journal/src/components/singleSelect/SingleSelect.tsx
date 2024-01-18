import { useEffect, useRef, useState } from "react";
import "./SingleSelect.css";
import { Link } from "react-router-dom";
import { AppRoute } from "../../const";

export type SelectOption = {
  label: string;
  value: string | number;
};

type SingleSelectProps = {
  value?: SelectOption;
  onChange: (value: SelectOption) => void;
};

type SelectProps = {
  options: SelectOption[];
} & SingleSelectProps;

export const Select = ({ value, onChange, options }: SelectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  function selectOption(option: SelectOption) {
    if (option !== value) onChange(option);
  }

  function isOptionSelected(option: SelectOption) {
    return option === value;
  }

  useEffect(() => {
    if (isOpen) setHighlightedIndex(0);
  }, [isOpen]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target != containerRef.current) return;
      switch (e.code) {
        case "Enter":
        case "Space":
          setIsOpen((prev) => !prev);
          if (isOpen) selectOption(options[highlightedIndex]);
          break;
        case "ArrowUp":
        case "ArrowDown": {
          if (!isOpen) {
            setIsOpen(true);
            break;
          }

          const newValue = highlightedIndex + (e.code === "ArrowDown" ? 1 : -1);
          if (newValue >= 0 && newValue < options.length) {
            setHighlightedIndex(newValue);
          }
          break;
        }
        case "Escape":
          setIsOpen(false);
          break;
      }
    };
    containerRef.current?.addEventListener("keydown", handler);

    return () => {
      containerRef.current?.removeEventListener("keydown", handler);
    };
  }, [isOpen, highlightedIndex, options]);

  return (
    <div className="organization-select">
      <div
        ref={containerRef}
        onBlur={() => setIsOpen(false)}
        onClick={() => setIsOpen((prev) => !prev)}
        tabIndex={0}
        className={"select-container"}
      >
        <span className={"select-value"}>{value?.label}</span>
        <div className={"select-caret"}></div>


        <ul className={`select-options ${isOpen ? "show" : ""}`}>
          {options.map((option, index) => (
            <li
              onClick={(e) => {
                e.stopPropagation();
                selectOption(option);
                setIsOpen(false);
              }}
              onMouseEnter={() => setHighlightedIndex(index)}
              key={option.value}
              className={`select-option ${
                isOptionSelected(option) ? "selected" : ""
              } ${index === highlightedIndex ? "highlighted" : ""}`}
            >
              {option.label}
            </li>
          ))}
        </ul>

      </div>
    </div>
  );
};
