import React from "react";
import { Header } from "../../components/header/Header";
import { AddEmployees } from "../../components/addEmployees/AddEmployees";
import { useParams } from "react-router-dom";

type CreateEmployeesPageProps = {};

function CreateEmployeesPage({}: CreateEmployeesPageProps): JSX.Element {
  const { organization } = useParams();
  return (
    <div>
      <Header />
      <AddEmployees organization={organization}/>
    </div>
  );
}

export default CreateEmployeesPage;
