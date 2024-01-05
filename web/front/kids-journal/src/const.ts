export const AppRoute = {
  WelcomeScreen: "/",
  Main: "/main",
  SignIn: "/login",
  SignUp: "/sign-up",
  Organizations: "/Organizations",
  Groups: "/groups",
  Activity: "/activity",
  Employees: "/employees",
  CreateActivity: "/createActivity",
  CreateGroups: "/createGroups",
  AddChild: "/addChild",
  Error: "/*",
};

export enum AuthorizationStatus {
  Auth = "AUTH",
  NoAuth = "NO_AUTH",
  Unknown = "UNKNOWN",
}

export const infoGroups = [
  {
    carouselLabel: "Одуванчики",
    carouselAge: "0-3",
    carouselAction: [
      {
        carouselActionData: "",
        carouselActionTitle: "Застегивание пуговиц",
        carouselActionCategory: "1",
      },
      { carouselActionTitle: "Клеим марки", carouselActionCategory: "2" },
    ],
    group_child: [
      {
        id: "",
        name: "Болтов Егор",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
      {
        id: "",
        name: "Болтов Егорp",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
    ],
  },
  {
    carouselLabel: "Ромашки",
    carouselAge: "3-6",
    carouselAction: [
      {
        carouselActionTitle: "Пить сок",
        carouselActionCategory: "2",
      },
    ],
    group_child: [
      {
        id: "",
        name: "Болтов Егор",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
    ],
  },
  {
    carouselLabel: "Васильки",
    carouselAge: "6-9",
    carouselAction: [
      {
        carouselActionTitle: "Застегивание пуговиц",
        carouselActionCategory: "1",
      },
    ],
  },
  {
    carouselLabel: "Васильки",
    carouselAge: "6-9",
    carouselAction: [
      {
        carouselActionTitle: "Застегивание пуговиц",
        carouselActionCategory: "1",
      },
    ],
    group_child: [
      {
        id: "",
        name: "Болтов Егор",
        birth_date: "2007-12-01",
        parents: [
          {
            id: "",
            name: "Болтова Инна Владимирована",
            phone_number: "+79998887766",
          },
        ],
      },
    ],
  },
];

export const infoEmployees = [
  {
    name: "Болтов Егор",
    role_id: "Администратор",
    phone_number: "+79998887766",
  },
  {
    name: "Викулова Света",
    role_id: "Педагог",
    phone_number: "+79998887766",
  },
];
