import { useMultistepForm } from "../../utils/helpers/form/useMultistepForm";
import { UserForm } from "../../components/userForm/UserForm";
import { DescriptionForm } from "../../components/userForm/DescriptionForm";
import React, { FormEvent, useState } from "react";
import { Header } from "../../components/header/Header";
import "./CreateActivityPage.css";
import { ApiRoute, AppRoute } from "../../const";
import { useNavigate, useParams } from "react-router-dom";

type FormData = {
  group: string;
  isIndividual: boolean;
  listChildren: [];
  date: string;
  subject: string;
  topic: string;
  description: string;
};

const INITIAL_DATA: FormData = {
  group: "",
  subject: "",
  topic: "",
  date: "",
  listChildren: [],
  description: "",
  isIndividual: false,
};

export default function CreateActivityPage() {
  const { organization } = useParams();
  const [data, setData] = useState(INITIAL_DATA);
  function updateFields(fields: Partial<FormData>) {
    setData((prev) => {
      return { ...prev, ...fields };
    });
  }

  const { steps, currentStepIndex, step, isFirstStep, back, next, isLastStep } =
    useMultistepForm([
      <UserForm {...data} updateFields={updateFields} />,
      <DescriptionForm {...data} updateFields={updateFields} />,
    ]);

  const navigate = useNavigate();

  function onSubmitForm(e: FormEvent) {
    e.preventDefault();
    if (!isLastStep) return next();
    else {
      const headers = new Headers();
      headers.append("Content-Type", "application/json");

      console.log(data.topic)

      let lesson = JSON.stringify({
        group_id: data.group,
        subject_id: data.subject,
        presentation_id: data.topic,
        start_lesson: data.date,
        child_id: data.listChildren.map(
          (child: { name: string; id: string }) => child.name,
        ),
        description: data.description,
      });
      console.log(lesson);

      let requestOptions = {
        method: "POST",
        headers: headers,
        body: lesson,
      };

      fetch(ApiRoute + `/lessons`, requestOptions);
    }
    navigate(`/${organization}${AppRoute.Main}`);
  }

  return (
    <>
      <Header />
      <div className="creat__text">Создание новой активности</div>
      <div className="creat_activity_container">
        <form onSubmit={onSubmitForm}>
          <div style={{ position: "absolute", top: ".5rem", right: ".5rem" }}>
            {currentStepIndex + 1}/{steps.length}
          </div>
          {step}
          <div
            style={{
              marginTop: "1rem",
              display: "flex",
              gap: ".5rem",
              justifyContent: "flex-end",
            }}
          >
            {!isFirstStep && (
              <button
                className="creat-button-activity"
                type="button"
                onClick={back}
              >
                Назад
              </button>
            )}
            <button className="creat-button-activity" type="submit">
              {isLastStep ? "Сохранить" : "Дальше"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}
