import React from "react";
import { Header } from "../../components/header/Header";
import { Employees } from "../../components/employees/Employees";

type EmployeesPageProps = {};

function EmployeesPage({}: EmployeesPageProps): JSX.Element {
    return (
        <div>
            <Header />
            <Employees />
        </div>
    );
}

export default EmployeesPage;
