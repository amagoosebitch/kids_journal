import React, { useState } from "react";
import { Button, CloseButton, Grid, GridItem, Input } from "@chakra-ui/react";
import { ButtonMain } from "../button/ButtonMain";

const options = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const optionsJob = [
  { job: "Администратор", value: 1 },
  { job: "Воспитатель", value: 2 },
  { job: "Нянечка", value: 3 },
];

export const AddEmployees = () => {
  const [value, setValue] = useState("");
  const [valueName, setName] = useState("");
  const [valueSurname, setSurname] = useState("");
  const [valueJob, setValueJob] = useState("");
  const [valueTel, setValueTel] = useState("");

  const addEmployees = () => {
    const result = {
      organization: value,
      name: valueName,
      surname: valueSurname,
      job: valueJob,
      tel: valueTel,
    };
    console.log(result);
  };

  return (
    <>
      <div className="creat__text">Создание новой группы</div>
      <div className="creat__form">
        <div>
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
              placeholder="Выберете должность"
              onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                setValueJob(event.currentTarget.value)
              }
            >
              {optionsJob.map((option) => (
                <option value={option.value}>{option.job}</option>
              ))}
            </select>
          </div>
          <div>
            <input
              type="text"
              placeholder="Введите имя"
              className="creat__form-select"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setName(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <input
              type="text"
              placeholder="Введите фамилию"
              className="creat__form-select"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setSurname(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <input
              type="tel"
              placeholder="Введите номер телефона"
              className="creat__form-select"
              onChange={(event: React.FormEvent<HTMLInputElement>) =>
                setValueTel(event.currentTarget.value)
              }
            />
          </div>
          <div>
            <ButtonMain
              className="creat__form-button"
              height="44px"
              width="211px"
              linkButton={""}
              onClick={() => addEmployees()}
            >
              Добавить сотрудника
            </ButtonMain>
          </div>
        </div>
      </div>
    </>
  );
};
