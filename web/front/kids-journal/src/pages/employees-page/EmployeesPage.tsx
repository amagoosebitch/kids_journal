import React from "react";
import { Header } from "../../components/header/Header";
import { Employees } from "../../components/employees/Employees";
import {useParams} from "react-router-dom";

type EmployeesPageProps = {};

function EmployeesPage({}: EmployeesPageProps): JSX.Element {
    const { organization } = useParams();
    return (
        <div>
            <Header />
            <Employees organization={organization} />
        </div>
    );
}

export default EmployeesPage;
