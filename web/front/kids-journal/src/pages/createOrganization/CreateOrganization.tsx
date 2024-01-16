import { Header } from "../../components/header/Header";
import React, { useState } from "react";
import "./CreateOrganization.css";
import { Input, Textarea } from "@chakra-ui/react";
import { ButtonMain } from "../../components/button/ButtonMain";

function CreateOrganization(): JSX.Element {
  const [valueName, setNameInput] = useState("");
  const [valueDescription, setValueDescription] = useState("");

  const addOrganization = {
    name: valueName,
    description: valueDescription,
  };

  function onSubmitForm() {
    return addOrganization;
  }

  return (
    <>
      <Header />
      <form className="create-organization-main__container">
        <div className="creat-organization__text">
          Создание новой организации
        </div>
        <div className="create-organization__form">
          <div className="create-organization">
            <div className="create-organization__form-items">
              <Input
                isRequired
                type="text"
                placeholder="Введите название организации"
                onChange={(event: React.FormEvent<HTMLInputElement>) =>
                  setNameInput(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              />
            </div>
            <div className="create-organization__form-items">
              <Textarea
                placeholder="Введите описание организации"
                onChange={(event: React.FormEvent<HTMLTextAreaElement>) =>
                  setValueDescription(event.currentTarget.value)
                }
                style={{
                  background: "white",
                }}
              />
            </div>
            <div className="create-organization__form-button">
              <ButtonMain
                typeButton="submit"
                className="create-organization__button"
                height="44px"
                width="211px"
                linkButton={""}
                onClick={onSubmitForm}
              >
                Создать организацию
              </ButtonMain>
            </div>
          </div>
        </div>
      </form>
    </>
  );
}
export default CreateOrganization;
