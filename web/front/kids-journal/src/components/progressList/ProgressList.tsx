import React, { useEffect, useState } from "react";
import { AppRoute, ApiRoute, infoGroups } from "../../const";
import { ButtonMain } from "../button/ButtonMain";
import "./ProgressList.css";
import { Link, useNavigate } from "react-router-dom";
import { AuthMiddleware } from "../../middlewares";
import {employeeInfo} from "../employees/Employees";

export type ProgressListProps = {
    organization: string | undefined;
};

export const groupInfo = [
    {
        group_id: "",
        organization_id: "",
        name: "",
        age_range: "",
        teacher: "",
    },
];

export const ProgressList = ({ organization }: ProgressListProps) => {
    const [firstProgress, setFirstProgress] = useState(groupInfo);
    useEffect(() => {
        fetch(`${ApiRoute}/organizations/${organization}/groups`, {
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
                setFirstProgress(data);
            });
    }, []);

    const [value, setValue] = useState("");
    const filteredGroups = firstProgress.filter((group) => {
        return group.name.toLowerCase().includes(value.toLowerCase());
    });

    return (
        <>
            <div className="progress__container">
                <div className="progress_title">Оценка прогресса</div>
                <div>
                    <ButtonMain
                        height="40px"
                        width="193px"
                        linkButton={`/${organization}${AppRoute.CreateGroups}`}
                    >
                        Сохранить изменения
                    </ButtonMain>
                </div>
            </div>

            <div className="progress">
                <table className="progress__table">
                    <thead className="progress-title">
                    <tr>
                        <td className="progress-title_label">Имя</td>
                        <td className="progress-title_age">Возраст</td>
                        <td className="progress-title_teach">Оценка</td>
                    </tr>
                    </thead>
                    <tbody>
                    {filteredGroups.map((group, index) => (
                        <tr className="progress-item">
                            <td className="progress-item_label">
                                <Link to={`/${organization}/${group.name}`}>
                                    {group.name}
                                </Link>
                            </td>
                            <td className="progress-item_age">{group.age_range}</td>
                            <td className="progress-item_teach">{group.group_id}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </>
    );
};
