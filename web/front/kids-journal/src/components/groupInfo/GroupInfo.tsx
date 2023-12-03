import React, { MouseEventHandler, useState } from "react";
import { Button } from "../button/Button";
import { AppRoute, infoGroups } from "../../const";
import { Link } from "react-router-dom";

import "./GroupInfo.css";
import { Modal } from "../modal/Modal";

export type GroupInfoProps = {
  groupId: string | undefined;
};

export const GroupInfo = ({ groupId }: GroupInfoProps) => {
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

  return (
    <>
      <div className="group_title">
        <div className="group_name">Группа {groupId}</div>
        <div>
          <Button
            height="44px"
            width="211px"
            linkButton={AppRoute.CreateGroups}
          >
            Добавить ребенка
          </Button>
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
            {currentGroup.map((group) => (
              <>
                {group.group_child?.map((child) => (
                  <>
                    <tr
                      className="children-item"
                      onClick={() =>
                        doDo(
                          child.name,
                          child.parents[0].name,
                          child.parents[0].phone_number,
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
                        {child.parents[0].phone_number}
                      </td>
                      <td className="children-item_parent">
                        {child.parents[0].name}
                      </td>
                    </tr>
                  </>
                ))}
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
