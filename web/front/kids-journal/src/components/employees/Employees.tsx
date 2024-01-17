import React, {useEffect, useState} from "react";
import { ButtonMain } from "../button/ButtonMain";
import {ApiRoute, AppRoute, infoEmployees} from "../../const";

import "./Employees.css";

export type EmployeesProps = {
  organization: string | undefined;
};

export const employeeInfo = [{
    group_id: '',
    organization_id: '',
    name: '',
    role_id:'',
    phone_number: ''
}]

export const Employees = ({ organization }: EmployeesProps) => {
    const [employees, setEmployees] = useState(employeeInfo);
    useEffect(() => {fetch(`${ApiRoute}/organizations/${organization}/employee`,
          {method: 'GET', headers: {'Accept': 'application/json',}}).then(response => {
          if (response.status === 200 || response.status === 201) {
              return response;
          }
          throw new Error();
      }).then(response => response.json()).then(data => {setEmployees(data)});
      }, [])

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
                <td className="employees-item_role_id">{employe.role_id}</td>
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
