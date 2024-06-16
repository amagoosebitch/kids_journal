import React, { useState } from "react";
import { Input, Select } from "@chakra-ui/react";
import { ButtonMain } from "../button/ButtonMain";
import "./AddEmployees.css";
import { InputPhone } from "../input-phone/InputPhone";
import {ApiRoute, AppRoute, testOrganization} from "../../const";

const options = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const optionsJob = [
  { job: "Администратор", value: 1 },
  { job: "Воспитатель", value: 2 },
];

type addEmployeeProps = {
  organization: string | undefined;
};

export const AddEmployees = ({ organization }: addEmployeeProps) => {
  const [valueName, setName] = useState("");
  const [valueSurname, setSurname] = useState("");
  const [valueJob, setValueJob] = useState("");
  const [valueTel, setValueTel] = useState("");

  const addEmployees = () => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    let employee = JSON.stringify({
      first_name: valueName,
      last_name: valueSurname,
      /*role_id: optionsJob[Number(valueJob) - 1].job,*/
      phone_number: valueTel,
    });

    let requestOptions1 = {
      method: "POST",
      headers: headers,
      body: employee,
    };

    fetch(
      ApiRoute + `/organizations/${testOrganization}/employee`,
      requestOptions1,
    );
  };

  return (
    <>
      <form className="creat-employees__container">
        <div className="creat__text">Добавление нового сотрудника</div>
        <div className="employees-creat__form">
          <div className="subject-creat">
            <div className="employees-creat__form-items">
              <Select
                placeholder="Выберите должность"
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
                onClick={() => addEmployees()}
                linkButton={`/${organization}${AppRoute.Employees}`}
              >
                Добавить сотрудника
                <svg
                    width="18"
                    height="10"
                    viewBox="0 0 18 10"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                      d="M12.707 9L15.9999 5.70711C16.3905 5.31658 16.3905 4.68342 15.9999 4.29289L12.707 1M15.707 5L1.70703 5"
                      stroke="white"
                      stroke-width="1.5"
                      stroke-linecap="round"
                  />
                </svg>
              </ButtonMain>
            </div>
          </div>
        </div>
      </form>
    </>
  );
};
