import React, { useEffect, useState } from "react";
import { ButtonMain } from "../button/ButtonMain";
import {ApiRoute, AppRoute, infoEmployees, testOrganization} from "../../const";

import "./Employees.css";

export type EmployeesProps = {
  organization: string | undefined;
};

export const employeeInfo = [
  {
    organization_id: "",
    name: "",
    phone_number: "",
  },
];

export const Employees = ({ organization }: EmployeesProps) => {
  const [employees, setEmployees] = useState(employeeInfo);
  useEffect(() => {
    fetch(`${ApiRoute}/organizations/${testOrganization}/employee`, {
      method: "GET",
      headers: { Accept: "application/json" },
    })
      .then((response) => {
        if (response.status === 200 || response.status === 201) {
          return response;
        }
        throw new Error();
      })
      .then((response) => response.json())
      .then((data) => {
        setEmployees(data);
      });
  }, []);

  console.log(employees)

  return (
    <>
      <div className="employees_title">
        <div className="employees_label">Сотрудники</div>
        <div>
          <ButtonMain
            height="44px"
            width="211px"
            linkButton={`/${organization}${AppRoute.CreateEmployees}`}
          >
            <svg
                width="14"
                height="14"
                viewBox="0 0 14 14"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
              <path
                  d="M1 7L13 7"
                  stroke="white"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
              />
              <path
                  d="M7 1L7 13"
                  stroke="white"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
              />
            </svg>
            Добавить сотрудника
          </ButtonMain>
        </div>
      </div>

      <div className="employees">
        <table className="employees__table">
          <thead className="employees-title">
            <tr>
              <td className="employees-title_name">Имя</td>
              <td className="employees-title_role_id">Роль</td>
              <td className="employees-phone_number">Контакт</td>
            </tr>
          </thead>
          <tbody>
            {employees.map((employe) => (
              <tr className="employees-item">
                <td className="employees-item_name">{employe.name}</td>
                <td className="employees-item_role_id">{employe.name}</td>
                <td className="employees-item_phone_number">
                  {employe.phone_number}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};
