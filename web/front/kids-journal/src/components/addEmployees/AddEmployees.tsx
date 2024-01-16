import React, { useState } from "react";
import { Input, Select } from "@chakra-ui/react";
import { ButtonMain } from "../button/ButtonMain";
import "./AddEmployees.css";
import { InputPhone } from "../input-phone/InputPhone";

const options = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const optionsJob = [
  { job: "Администратор", value: 1 },
  { job: "Воспитатель", value: 2 },
];

export const AddEmployees = () => {
  const [value, setValue] = useState("");
  const [valueName, setName] = useState("");
  const [valueSurname, setSurname] = useState("");
  const [valueJob, setValueJob] = useState("");
  const [valueTel, setValueTel] = useState("");

  const addEmployees = () => {
    const result = {
      organization_id: value,
      name: valueName,
      surname: valueSurname,
      job: valueJob,
      tel: valueTel,
    };
  };

  return (
    <>
      <form className="creat-employees__container">
        <div className="creat__text">Добавление нового сотрудника</div>
        <div className="employees-creat__form">
          <div className="subject-creat">
            <div className="employees-creat__form-items">
              <Select
                placeholder="Выберете организацию"
                onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                  setValue(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              >
                {options.map((option) => (
                  <option value={option.value}>{option.label}</option>
                ))}
              </Select>
            </div>
            <div className="employees-creat__form-items">
              <Select
                placeholder="Выберете должность"
                onChange={(event: React.FormEvent<HTMLSelectElement>) =>
                  setValueJob(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              >
                {optionsJob.map((option) => (
                  <option value={option.value}>{option.job}</option>
                ))}
              </Select>
            </div>
            <div className="employees-creat__form-items">
              <Input
                type="text"
                placeholder="Введите имя"
                onChange={(event: React.FormEvent<HTMLInputElement>) =>
                  setName(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              />
            </div>
            <div className="employees-creat__form-items">
              <Input
                type="text"
                placeholder="Введите фамилию"
                onChange={(event: React.FormEvent<HTMLInputElement>) =>
                  setSurname(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              />
            </div>
            <div className="employees-creat__form-items">
              <InputPhone
                onChange={(event: React.FormEvent<HTMLInputElement>) =>
                  setValueTel(event.currentTarget.value)
                }
              />
            </div>
            <div className="creat-employees__form-button">
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
      </form>
    </>
  );
};
