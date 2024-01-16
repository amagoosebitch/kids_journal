import { FormWrapper } from "./FormWrapper";
import { Checkbox, Input, Select } from "@chakra-ui/react";
import { useState } from "react";
import { Multiselect } from "multiselect-react-dropdown";

type UserData = {
  group: string;
  isIndividual: boolean;
  listChildren: [];
  date: string;
};

type UserFormProps = UserData & {
  updateFields: (fields: Partial<UserData>) => void;
};

const groupsData = [
  { label: "Садик №1", value: 1 },
  { label: "Садик Вишенка", value: 2 },
];

const childrenData = [
  { id: 1, name: "Болтов Егор" },
  { id: 2, name: "Болтов Егорp" },
];

export function UserForm({
  group,
  isIndividual,
  listChildren,
  date,
  updateFields,
}: UserFormProps) {
  const [options] = useState(childrenData);

  console.log(date)

  return (
    <FormWrapper>
      <label>Группа</label>
      <Select
        required
        value={group}
        onChange={(e) => updateFields({ group: e.target.value })}
        style={{
          background: "white",
        }}
      >
        {groupsData.map((group) => (
          <option value={group.value}>{group.label}</option>
        ))}
      </Select>
      <label>Дата</label>
      <Input
        required
        type="datetime-local"
        value={date}
        onChange={(e) => updateFields({ date: e.target.value })}
        style={{
          background: "white",
        }}
      />
      <input
        type="checkbox"
        checked={isIndividual}
        onChange={(e) =>
          updateFields({ isIndividual: e.currentTarget.checked })
        }
      />
      Индивидуальное задание
      {isIndividual && (
        <>
          <label>Дети</label>
          <Multiselect
            options={options}
            displayValue="name"
            placeholder='Выберите ребенка'
          />
        </>
      )}
    </FormWrapper>
  );
}
