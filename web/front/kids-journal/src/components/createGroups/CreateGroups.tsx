import "./CreateGroups.css";
import React, { useState } from "react";
import { Select } from "@chakra-ui/react";
import { Button } from "../button/Button";

const options = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const optionsAge = [
  { age: "0-3", value: 1 },
  { age: "3-6", value: 2 },
  { age: "6-9", value: 3 },
];

export const CreateGroups = () => {
  const [value, setValue] = useState("");
  const [valueAge, setValueAge] = useState("");
  const [valueInput, setValueInput] = useState("");

  return (
    <>
      <div className="creat__text">Создание новой группы</div>
      <div className="creat__form">
        <div>
          <select
            className="creat__form-select"
            placeholder="Выберете организацию"
            onChange={(event: React.FormEvent<HTMLSelectElement>) =>
              setValue(event.currentTarget.value)
            }
          >
            {options.map((option) => (
              <option value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
        <div>
          <select
            className="creat__form-select"
            placeholder="Выберете возраст детей"
            onChange={(event: React.FormEvent<HTMLSelectElement>) =>
              setValueAge(event.currentTarget.value)
            }
          >
            {optionsAge.map((option) => (
              <option value={option.value}>{option.age}</option>
            ))}
          </select>
          <div>
            <input
              type="text"
              placeholder="Введите название группы"
              className="creat__form-select"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setValue(event.currentTarget.value)
              }
            />
          </div>

          <div>
            <Button
              className="creat__form-button"
              height="44px"
              width="211px"
              linkButton={""}
            >
              Создать группу
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};
