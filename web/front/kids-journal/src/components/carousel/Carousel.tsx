import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Carousel.css";

import Slider from "react-slick";
import { useEffect, useState } from "react";

import { infoGroups, ApiRoute } from "../../const";
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

export const groupInfo = [
  {
    group_id: "",
    organization_id: "",
    name: "",
    age_range: "",
  },
];

type lessonInfoProps = [
  {
    schedule_id: string;
    subject_name: string;
    group_name: string;
    child_names: string[];
    date: Date;
    description: string;
    is_for_child: boolean;
  },
];

export const lessonInfo: lessonInfoProps = [
  {
    schedule_id: "",
    subject_name: "",
    group_name: "",
    child_names: [""],
    date: new Date(),
    description: "",
    is_for_child: false,
  },
];

export const Carousel = ({ organization, currentDate }: CarouselProps) => {
  const [carousels, setCarousels] = useState(infoGroups);

  const currentCarousel = carousels.filter((carousel) => {
    if (organization !== undefined)
      return carousel.organization
        .toLowerCase()
        .includes(organization.toLowerCase());
    return {};
  });

  const [groups, setGroups] = useState(groupInfo);
  const [lesson, setLesson] = useState(lessonInfo);
  const [allInfo, setAllInfo] = useState([{ group: "", lessons: lessonInfo }]);

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

    for (let i = 1; i < groups.length; i++) {
      fetch(`${ApiRoute}/lessons/${groups[i].group_id}?date=${currentDate}`, {
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
          setLesson(data);
        })
        .then(() =>
          setAllInfo([...allInfo, { group: groups[i].group_id, lessons: lesson }]),
        );
    }
  }, []);


  let slidesToShowCurrent = 3;
  if (currentCarousel.length === 1) slidesToShowCurrent = 1;
  if (currentCarousel.length === 2) slidesToShowCurrent = 2;

  let settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: slidesToShowCurrent,
    slidesToScroll: 3,
    initialSlide: 0,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: slidesToShowCurrent === 1 ? 1 : slidesToShowCurrent - 1,
          slidesToScroll:
            slidesToShowCurrent === 1 ? 1 : slidesToShowCurrent - 1,
          infinite: true,
          dots: true,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          initialSlide: 1,
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

  const formatData = currentDate.toLocaleDateString();

  const [isOpenModal, setIsOpenModal] = useState(false);

  const [currentActivity, setCurrentActivity] = useState(action1);
  const [currentGroup, setCurrentGroup] = useState("");

  const doDo = (action: ActionProps, group: string) => {
    setCurrentActivity(action);
    setCurrentGroup(group);
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
              <div className="carousel_box-content">
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
