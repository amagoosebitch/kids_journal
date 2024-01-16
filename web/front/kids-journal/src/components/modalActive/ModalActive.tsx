import clsx from "clsx";
import { useState, useEffect } from "react";
import type { ReactNode, FC } from "react";
import { default as ReactModal } from "react-responsive-modal";
import "react-responsive-modal/styles.css";
import "./ModalActive.css";
import { CloseButton } from "@chakra-ui/react";
import { ActionProps } from "../carousel/Carousel";

type IModalSize = "medium";

type TModalProps = {
  topic?: string;
  children?: ReactNode;
  className?: string;
  dataTestId?: string;
  isOpen: boolean;
  currentGroup: string;
  currentActivity: {
    carouselActionData: string;
    subject: string;
    carouselActionTitle: string;
    carouselActionCategory: boolean;
    children: {
      name: string;
    }[];
    description: string;
  };
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
        <div className="Modal_content">
          <tr className="Modal_content-item">
            <td className="la Modal_content-group">Группа</td>
            <td className='Modal_content-information'>{currentGroup}</td>
          </tr>
          <tr className="Modal_content-item">
            <td className="la Modal_content-topic">Предмет</td>
            <td className='Modal_content-information'>{currentActivity.subject}</td>
          </tr>
          <tr className="Modal_content-item">
            <td className="la Modal_content-topic">Тема</td>
            <td className='Modal_content-information'>{currentActivity.carouselActionTitle}</td>
          </tr>
          <tr className="Modal_content-item">
            <td className="la Modal_content-date">Дата</td>
            <td className='Modal_content-information'>{new Date(currentActivity.carouselActionData).toLocaleDateString()}</td>
          </tr>
          <tr className="Modal_content-item">
            <td className="la Modal_content-time">Время</td>
            <td className='Modal_content-information'>{currentActivity.carouselActionData.split('T')[1]}</td>
          </tr>
          <tr className="Modal_content-item">
            <td className="la Modal_content-description">Описание</td>
            <td className='Modal_content-information'>{currentActivity.description}</td>
          </tr>
          <tr className="Modal_content-item">
            {currentActivity.carouselActionCategory ? (
              <div>Индивидуальное задание</div>
            ) : (
              <div>Задание для всей группы</div>
            )}
          </tr>
          <tr className="Modal_content-item">
            {currentActivity.carouselActionCategory && (
              <>
                <td className="la Modal_content-children">Дети</td>
                <td className='Modal_content-information'>
                  {currentActivity.children.map((child) => (
                      <tr>{child.name}</tr>
                  ))}
                </td>
              </>
            )}
          </tr>
        </div>
      </div>
    </ReactModal>
  );
};
