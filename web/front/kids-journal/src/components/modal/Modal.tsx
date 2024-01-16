import clsx from "clsx";
import { useState, useEffect } from "react";
import type { ReactNode, FC } from "react";
import { default as ReactModal } from "react-responsive-modal";
import "react-responsive-modal/styles.css";
import "./Modal.css";
import { CloseButton } from "@chakra-ui/react";

type IModalSize = "medium";

type TModalProps = {
    children?: ReactNode;
    className?: string;
    dataTestId?: string;
    isOpen: boolean;
    onCloseModal: () => void;
    currChild: string[];
    groupId: string| undefined;
    size?: IModalSize;
};

export const Modal = ({
                          children,
                          currChild,
                          groupId,
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
                <div className="Modal-img"></div>
                <div className="Modal_content">
                    <div className="Modal-name">{currChild[0]}</div>
                    <div className="Modal_text">
                        <div className="Modal_text-label">Группа {groupId}</div>
                        <div className="Modal_text-parent">
                            <div className="Modal_text-parent_name">
                                Родитель: {currChild[1]}
                            </div>
                            <div className="Modal_text-parent_number">{currChild[2]}</div>
                        </div>
                    </div>
                </div>
            </div>
        </ReactModal>
    );
};
