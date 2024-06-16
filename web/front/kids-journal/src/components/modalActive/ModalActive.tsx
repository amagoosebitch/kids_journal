import clsx from "clsx";
import { useState, useEffect } from "react";
import type { ReactNode, FC } from "react";
import { default as ReactModal } from "react-responsive-modal";
import "react-responsive-modal/styles.css";
import "./ModalActive.css";
import { CloseButton } from "@chakra-ui/react";
import { ApiRoute, AppRoute } from "../../const";
import { ButtonMain } from "../button/ButtonMain";
import { useParams } from "react-router-dom";

type IModalSize = "medium";

type lessonInfoProps = [
  {
    schedule_id: string;
    presentation_id: string;
    child_ids: string[];
    date_day: string;
    is_for_child: boolean;
  },
];

type TModalProps = {
  topic?: string;
  children?: ReactNode;
  className?: string;
  dataTestId?: string;
  isOpen: boolean;
  currentGroup: string;
  currentActivity: lessonInfoProps;
  onCloseModal: () => void;
  size?: IModalSize;
};

export const ModalActive = ({
  currentGroup,
  currentActivity,
  className,
  isOpen,
  onCloseModal,
  size = "medium",
}: TModalProps): JSX.Element => {
  const defaultClassNames = {
    modal: clsx("ModalDefault", className, {
      ModalDefault__medium: size === "medium",
    }),
    closeButton: clsx("ModalDefaultCloseButton"),
  };
  const [styles, setStyles] = useState({});
  const { organization } = useParams();

  useEffect(() => {
    const scrollbarWidth =
      window.innerWidth - document.documentElement.clientWidth;
    if (isOpen && scrollbarWidth) {
      const _styles = {
        modal: { marginRight: `${scrollbarWidth + 16}px` },
      };
      setStyles(_styles);
      document.body.classList.add("Modal__open");
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }

    return () => {
      setStyles({});
      document.body.style.removeProperty("padding-right");
      document.body.classList.remove("Modal__open");
    };
  }, [isOpen]);

  return (
    <ReactModal
      center
      classNames={defaultClassNames}
      closeIcon={<CloseButton />}
      onClose={onCloseModal}
      open={isOpen}
      styles={styles}
    >
      <div className="Modal">
        <div className="Modal_header">
          <div className="Modal_header-subject_name">
            {currentActivity[0].schedule_id}
          </div>
          <div className="Modal_header-data">
            {currentActivity[0].date_day.split("T")[0]}
          </div>
        </div>
        <div className="Modal_content">
          <div className="Modal_content-item">
            <div className="Modal_content-group">Группа:</div>
            <div className="Modal_content-information">{currentGroup}</div>
          </div>
          <div className="Modal_content-item">
            <div className="Modal_content-topic">Тема:</div>
            <div className="Modal_content-information">
              {currentActivity[0].presentation_id}
            </div>
          </div>
          <div className="Modal_content-item">
            <div className="Modal_content-time">Время:</div>
            <div className="Modal_content-information">
              {currentActivity[0].date_day
                .split("T")[1]
                ?.split(":")
                .slice(0, -1)
                .join(":")}
            </div>
          </div>
          <div className="Modal_content-item">
            {currentActivity[0].is_for_child ? (
              <>
                <div className="Modal_content-children">Ученики:</div>
                <div className="Modal_content-information">
                  {currentActivity[0].child_ids.map((child) => (
                    <div>{child}</div>
                  ))}
                </div>
              </>
            ) : (
              <div>Задание для всей группы</div>
            )}
          </div>
        </div>
        <div className="Modal_footer">
          <div>
            <ButtonMain
              height="40px"
              width="168px"
              linkButton={`/${organization}/${currentGroup}/${currentActivity[0].schedule_id}${AppRoute.Progress}`}
            >
              Выставить оценки
            </ButtonMain>
          </div>
          <div>
            <ButtonMain
              height="40px"
              width="145px"
              linkButton={`/${organization}/${currentGroup}/${
                currentActivity[0].schedule_id
              }/${currentActivity[0].date_day.split("T")[0]}/${
                currentActivity[0].schedule_id
              }`}
            >
              Редактировать
            </ButtonMain>
          </div>
          <div>
            <ButtonMain height="40px" width="98px" linkButton={``}>
              Удалить
            </ButtonMain>
          </div>
        </div>
      </div>
    </ReactModal>
  );
};
