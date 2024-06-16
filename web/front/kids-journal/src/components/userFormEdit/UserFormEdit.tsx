import { FormWrapperEdit } from "./FormWrapperEdit";
import { Checkbox, Input, Select } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { Multiselect } from "multiselect-react-dropdown";
import { ApiRoute } from "../../const";
import { useParams } from "react-router-dom";
import {childInfo, groupInfo} from "../userForm/UserForm";

type UserData = {
  group: string;
  isIndividual: boolean;
  listChildren: [];
  date: string;
};

type UserFormProps = UserData & {
  updateFields: (fields: Partial<UserData>) => void;
};

const childrenData = [
  { id: 1, name: "Болтов Егор" },
  { id: 2, name: "Болтов Егорp" },
];

export function UserFormEdit({
  group,
  isIndividual,
  listChildren,
  date,
  updateFields,
}: UserFormProps) {
  const { organization } = useParams();
  const [options] = useState(childrenData);

  const [groups, setGroups] = useState(groupInfo);
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
        setGroups(data);
      });
  }, []);

  const [curGroup, setCurGroup] = useState("");
  const handleGroupsName = (e: string) => {
    return groups[Number(e)].name;
  };

  const [chilgren, setChilgren] = useState(childInfo);

  useEffect(() => {
    if (curGroup !== "") {
      fetch(`${ApiRoute}/${curGroup}/child`, {
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
          setChilgren(data);
        });
    }
  }, [curGroup]);

  return (
    <FormWrapperEdit>
      <label>Группа</label>
      <Select
        required
        placeholder="Выберите группу"
        onClick={(e) => setCurGroup(handleGroupsName(e.currentTarget.value))}
        onChange={(e) =>
          updateFields({ group: handleGroupsName(e.target.value) })
        }
        style={{
          background: "white",
        }}
      >
        {groups.map((groupCur, index) => (
          <option value={index}>{groupCur.name}</option>
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
            options={chilgren.map((child, index) => ({
              name: child.child_id,
              id: index,
            }))}
            displayValue="name"
            placeholder="Выберите ребенка"
            selectedValues={listChildren}
            onSelect={(e) => updateFields({ listChildren: e })}
            onRemove={(e) => updateFields({ listChildren: e })}
          />
        </>
      )}
    </FormWrapperEdit>
  );
}
