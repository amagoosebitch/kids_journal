import { useMultistepForm } from "../../utils/helpers/form/useMultistepForm";
import { ButtonMain } from "../../components/button/ButtonMain";
import { UserForm } from "../../components/userForm/UserForm";
import { DescriptionForm } from "../../components/userForm/DescriptionForm";
import React, { FormEvent, useState } from "react";
import { Header } from "../../components/header/Header";
import "./CreateActivityPage.css";

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
  isIndividual: false,
  listChildren: [],
  date: "",
  subject: "",
  topic: "",
  description: "",
};

export default function CreateActivityPage() {
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

  function onSubmitForm(e: FormEvent) {
    e.preventDefault();
    return !isLastStep ? next() : alert("GOOD!!!");
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
              <button type="button" onClick={back}>
                Назад
              </button>
            )}
            <button type="submit">{isLastStep ? "Сохранить" : "Дальше"}</button>
          </div>
        </form>
      </div>
    </>
  );
}
