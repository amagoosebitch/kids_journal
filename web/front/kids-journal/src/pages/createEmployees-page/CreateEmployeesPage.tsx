import React from "react";
import { Header } from "../../components/header/Header";
import {AddEmployees} from "../../components/addEmployees/AddEmployees";

type CreateEmployeesPageProps = {};

function CreateEmployeesPage({}: CreateEmployeesPageProps): JSX.Element {
  return (
    <div>
      <Header />
      <AddEmployees />
    </div>
  );
}

export default CreateEmployeesPage;
