import React, {MouseEventHandler, useEffect, useState} from "react";
import { ButtonMain } from "../button/ButtonMain";
import {ApiRoute, AppRoute, infoGroups} from "../../const";
import { Link } from "react-router-dom";

import "./GroupInfo.css";
import { Modal } from "../modal/Modal";
import {groupInfo} from "../groups/Groups";

export type GroupInfoProps = {
  groupId: string | undefined;
  organization: string | undefined;
};

export const parent = {
    parent_id:'',
    name:'',
    phone_number:'',
}

export const child = {
    name:'',
    birth_date:new Date(),
    parent_1: {
            name:'',
            phone_number:'',
    },
    parent_2:{
            name:'',
            phone_number:'',
    },
}



export const GroupInfo = ({ organization, groupId }: GroupInfoProps) => {
  const [children, setChildren] = useState([child]);
    useEffect(() => {fetch(`${ApiRoute}/${groupId}/child`,
          {method: 'GET', headers: {'Accept': 'application/json',}}).then(response => {
          if (response.status === 200 || response.status === 201) {
              return response;
          }
          throw new Error();
      }).then(response => response.json()).then(data => {setChildren(data)});
      }, [])
  const [groups, setGroups] = useState(infoGroups);

  const currentGroup = groups.filter((group) => {
    if (groupId !== undefined)
      return group.carouselLabel.toLowerCase().includes(groupId.toLowerCase());
    return {};
  });

  const [isOpenModal, setIsOpenModal] = useState(false);

  const [currChild, setCurrChild] = useState([""]);

  const doDo = (name: string, parent: string, number: string) => {
    setCurrChild([name, parent, number]);
  };

  const handleModalOpen = () => {
    setIsOpenModal(true);
  };

  const handleModalClose = () => {
    setIsOpenModal(false);
  };

  console.log(children);

  return (
    <>
      <div className="group_title">
        <div className="group_name">Группа {groupId}</div>
        <div>
          <ButtonMain
            height="44px"
            width="211px"
            linkButton={`/${organization}/${groupId}${AppRoute.AddChild}`}
          >
            Добавить ребенка
          </ButtonMain>
        </div>
      </div>

      <div className="children">
        <table className="children__table">
          <thead className="children-title">
            <tr>
              <td className="children-title_name">Имя</td>
              <td className="children-title_age">Возраст</td>
              <td className="children-phone_number">Контакт родителей</td>
              <td className="children-parent">Имя родителя</td>
            </tr>
          </thead>
          <tbody>
                {children?.map((child) => (
                  <>
                    <tr
                      className="children-item"
                      onClick={() =>
                        doDo(
                          child.name,
                          child.parent_1.name,
                          child.parent_1.phone_number,
                        )
                      }
                    >
                      <td className="children-item_name">
                        <Link to={""} onClick={handleModalOpen}>
                          {child.name}
                        </Link>
                      </td>
                      <td className="children-item_age">
                        {new Date().getFullYear() -
                          new Date(child.birth_date).getFullYear()}
                      </td>
                      <td className="children-item_number">
                        {child.parent_1.phone_number}
                      </td>
                      <td className="children-item_parent">
                        {child.parent_1.name}
                      </td>
                    </tr>
                  </>
                ))}
          </tbody>
        </table>
      </div>
      <Modal
        isOpen={isOpenModal}
        onCloseModal={handleModalClose}
        groupId={groupId}
        currChild={currChild}
      />
    </>
  );
};
