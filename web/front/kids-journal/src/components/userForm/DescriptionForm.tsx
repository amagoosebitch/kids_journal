import { FormWrapper } from "./FormWrapper";
import { Input, Select } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { ApiRoute, testOrganization } from "../../const";
import { useParams } from "react-router-dom";

type DescriptionDate = {
  subject: string;
  topic: string;
  description: string;
};

type DescriptionFormProps = DescriptionDate & {
  updateFields: (fields: Partial<DescriptionDate>) => void;
};

export const infoSubject = [
  {
    subject_id: "",
    name: "",
    description: "",
    age_range: "",
  },
];

export const infoTopic = [
  {
    presentation_id: "",
    name: "",
    description: "",
    photo_url: "",
    file_url: "",
    subject_id: "",
  },
];

export function DescriptionForm({
  subject,
  topic,
  description,
  updateFields,
}: DescriptionFormProps) {
  const { organization } = useParams();

  const [subjects, setSubjects] = useState(infoSubject);
  const [presentations, setPresentations] = useState(infoTopic);

  const [curSubject, setCurSubject] = useState("");
  useEffect(() => {
    fetch(`${ApiRoute}/organizations/${testOrganization}/subjects`, {
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
        setSubjects(data);
      });
  }, []);

  useEffect(() => {
    if (curSubject !== "") {
      setPresentations(infoTopic);
      fetch(`${ApiRoute}/subjects/${curSubject}/presentations`, {
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
          setPresentations(data);
        });
    }
  }, [curSubject]);

  const handleSubjectName = (e: string) => {
    return subjects[Number(e)].subject_id;
  };

  const handleTopicName = (e: string) => {
    return presentations[Number(e)].name;
  };

  return (
    <FormWrapper>
      <label>Предмет</label>
      <Select
        required
        placeholder="Выберите предмет"
        onClick={(e) => setCurSubject(handleSubjectName(e.currentTarget.value))}
        onChange={(e) =>
          updateFields({ subject: handleSubjectName(e.target.value) })
        }
        style={{
          background: "white",
        }}
      >
        {subjects.map((subject, index) => (
          <option value={index}>{subject.name}</option>
        ))}
      </Select>
      <label>Тема</label>
      <Select
        required
        placeholder="Выберите тему"
        onChange={(e) =>
          updateFields({ topic: handleTopicName(e.target.value) })
        }
        style={{
          background: "white",
        }}
      >
        {presentations?.map((presentation, index) => (
          <option value={index}>{presentation.name}</option>
        ))}
      </Select>
      <label>Описание</label>
      <Input
        type="text"
        value={description}
        onChange={(e) => updateFields({ description: e.target.value })}
        style={{
          background: "white",
        }}
      />
    </FormWrapper>
  );
}
