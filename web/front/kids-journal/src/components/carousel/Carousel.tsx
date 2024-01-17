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

// export type ActionProps = {
//   carouselActionData: string;
//   carouselActionTitle: string;
//   subject: string;
//   carouselActionCategory: boolean;
//   children: {
//     name: string;
//   }[];
//   description: string;
// };

export type ActionProps = {
  group_id: string;
  subject_id: string;
  start_lesson: Date;
  presentation_id: string;
  child_id: [],
  description: string;
};

// const action1 = {
//   carouselActionData: "",
//   carouselActionTitle: "",
//   subject: "",
//   carouselActionCategory: true,
//   children: [
//     {
//       name: "",
//     },
//   ],
//   description: "",
// };

export const groupInfo = [
  {
    group_id: "",
    organization_id: "",
    name: "",
    age_range: "",
  },
];

export const scheduleInfo = [
  {
    group_id: "",
    subject_id: "",
    start_lesson: new Date(),
    presentation_id: "",
    child_id: [],
    description: "",
  },
];

export const Carousel = ({ organization, currentDate }: CarouselProps) => {
  // const [carousels, setCarousels] = useState(infoGroups);
  //
  // const currentCarousel = carousels.filter((carousel) => {
  //   if (organization !== undefined)
  //     return carousel.organization
  //       .toLowerCase()
  //       .includes(organization.toLowerCase());
  //   return {};
  // });

  const [firstGroups, setFirstGroups] = useState(groupInfo);
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
        setFirstGroups(data);
      });
  }, []);

  const [subjects, setSubjects] = useState(scheduleInfo);

  const currentAction = (group_id: string) => {
    useEffect(() => {
      fetch(`${ApiRoute}/lessons/${group_id}`, {
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
          setSubjects(data);
        });
    }, []);
    return subjects;
  };

  console.log(firstGroups);

  let slidesToShowCurrent = 3;

  if (firstGroups.length === 1) slidesToShowCurrent = 1;
  if (firstGroups.length === 2) slidesToShowCurrent = 2;

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

  const [currentActivity, setCurrentActivity] = useState(scheduleInfo);
  const [currentGroup, setCurrentGroup] = useState("");

  // const doDo = (action: ActionProps, group: string) => {
  //   setCurrentActivity(action);
  //   setCurrentGroup(group);
  // };

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
          {firstGroups.map((carousel) => (
            <div className="carousel_box">
              <div className="carousel_box-title">
                <div className="carousel_box-name">Группа {carousel.name}</div>
                <div className="carousel_box-age">{carousel.age_range}</div>
              </div>
              <div className="carousel_box-content">
                {currentAction(carousel.name)
                  .filter((action) => {
                    return (
                      action.start_lesson.toLocaleDateString() === formatData
                    );
                  })
                  .map((action) => (
                    <Link to={""} onClick={handleModalOpen}>
                      <div
                        className={`carousel_box-action ${
                          action.child_id ? "isOrange" : "isGreen"
                        }`}
                      >
                        <div className="carousel_action-info">
                          <div className="carousel_action-topic">
                            {action.presentation_id}
                          </div>
                          <div className="carousel_action-time">
                            {action.start_lesson.toLocaleDateString()}
                          </div>
                        </div>
                        <div className="carousel_action-children">
                          {action.child_id &&
                            `Дети: ${action.child_id[0]} ${
                              action.child_id.length > 1
                                ? `и еще ${action.child_id.length - 1}`
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
      {/*<ModalActive*/}
      {/*  isOpen={isOpenModal}*/}
      {/*  onCloseModal={handleModalClose}*/}
      {/*  currentActivity={currentActivity}*/}
      {/*  currentGroup={currentGroup}*/}
      {/*/>*/}
    </>
  );
};
