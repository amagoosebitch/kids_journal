import { FormWrapper } from "./FormWrapper";
import { Input } from "@chakra-ui/react";

type DescriptionDate = {
  subject: string;
  topic: string;
  description: string;
};

type DescriptionFormProps = DescriptionDate & {
  updateFields: (fields: Partial<DescriptionDate>) => void;
};

export function DescriptionForm({
  subject,
  topic,
  description,
  updateFields,
}: DescriptionFormProps) {
  return (
    <FormWrapper>
      <label>Предмет</label>
      <Input
        required
        type="text"
        value={subject}
        onChange={(e) => updateFields({ subject: e.target.value })}
        style={{
          background: "white",
        }}
      />
      <label>Тема</label>
      <Input
        required
        type="text"
        value={topic}
        onChange={(e) => updateFields({ topic: e.target.value })}
        style={{
          background: "white",
        }}
      />
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
