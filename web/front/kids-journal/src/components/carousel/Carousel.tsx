import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Carousel.css";

import Slider from "react-slick";
import { useState } from "react";

import { infoGroups } from "../../const";
import { Link } from "react-router-dom";
import { ModalActive } from "../modalActive/ModalActive";

export type CarouselProps = {
  organization: string | undefined;
  currentDate: Date;
};

export type ActionProps = {
  carouselActionData: string;
  carouselActionTitle: string;
  subject: string;
  carouselActionCategory: boolean;
  children: {
    name: string;
  }[];
  description: string;
};

const action1 = {
  carouselActionData: "",
  carouselActionTitle: "",
  subject: "",
  carouselActionCategory: true,
  children: [
    {
      name: "",
    },
  ],
  description: "",
};

export const Carousel = ({ organization, currentDate }: CarouselProps) => {
  let settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 3,
    initialSlide: 0,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 3,
          infinite: true,
          dots: true,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          initialSlide: 2,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  const [carousels, setCarousels] = useState(infoGroups);

  const currentCarousel = carousels.filter((carousel) => {
    if (organization !== undefined)
      return carousel.organization
        .toLowerCase()
        .includes(organization.toLowerCase());
    return {};
  });

  const formatData = currentDate.toLocaleDateString();

  const [isOpenModal, setIsOpenModal] = useState(false);

  const [currentActivity, setCurrentActivity] = useState(action1);
  const [currentGroup, setCurrentGroup] = useState('');

  const doDo = (action: ActionProps, group: string) => {
    setCurrentActivity(action);
    setCurrentGroup(group)
  };

  const handleModalOpen = () => {
    setIsOpenModal(true);
  };

  const handleModalClose = () => {
    setIsOpenModal(false);
  };

  return (
    <>
      <div className="carousel">
        <Slider {...settings}>
          {currentCarousel.map((carousel) => (
            <div className="carousel_box">
              <div className="carousel_box-title">
                <div className="carousel_box-name">
                  Группа {carousel.carouselLabel}
                </div>
                <div className="carousel_box-age">{carousel.carouselAge}</div>
              </div>
              {carousel.carouselAction
                .filter((action) => {
                  return (
                    new Date(
                      action.carouselActionData.split("T")[0],
                    ).toLocaleDateString() === formatData
                  );
                })
                .map((action) => (
                  <Link to={""} onClick={handleModalOpen}>
                    <div
                      onClick={() => doDo(action, carousel.carouselLabel)}
                      className={`carousel_box-action ${
                        action.carouselActionCategory ? "isOrange" : "isGreen"
                      }`}
                    >
                      <div className="carousel_action-info">
                        <div className="carousel_action-topic">
                          {action.carouselActionTitle}
                        </div>
                        <div className="carousel_action-time">
                          {action.carouselActionData.split("T")[1]}
                        </div>
                      </div>
                      <div className="carousel_action-children">
                        {action.carouselActionCategory &&
                          `Дети: ${action.children[0].name} ${
                            action.children.length > 1
                              ? `и еще ${action.children.length - 1}`
                              : ""
                          }`}
                      </div>
                    </div>
                  </Link>
                ))}
            </div>
          ))}
        </Slider>
      </div>
      <ModalActive
        isOpen={isOpenModal}
        onCloseModal={handleModalClose}
        currentActivity={currentActivity}
        currentGroup={currentGroup}
      />
    </>
  );
};
