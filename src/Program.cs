using System;
using System.Linq;
using Shine;
using Shine.Middleware.Session;
using Shine.Responses;
using Shine.Routing;
using Shine.Server.HttpListener;
using Shine.Templates.DotLiquid;
using Shine.Utilities;

namespace PsycologicalWebTest
{
    class Program
    {
        private static readonly ParticipantManager Participants = 
            new ParticipantManager("D:\\TestResults\\participants.json");

        private static readonly TestsManager TestsManager =
            new TestsManager("../../tests.json", "D:\\TestResults\\");
         
        static void Main(string[] args)
        {
            var rootRouter = new Router();
            rootRouter.Bind("^/static", new StaticServeRouter("../../static"));
            rootRouter.Bind("^/favicon.ico", request => null);
            rootRouter.Bind("^/$", Home);
            rootRouter.Bind("^/start", Start);
            rootRouter.Bind("^/result", Result);
            rootRouter.Bind("^/test/(.+)", Test);

            var templateEngine = new DotLiquidTemplateProcessor("../../Templates");
            templateEngine.RegisterSafeType<Test>();
            templateEngine.RegisterSafeType<Participant>();

            var app = new App(rootRouter);
            app.SetTemplateProcessor(templateEngine);
            app.RegisterMiddleware(new SessionMiddleware("SECRET KEY"));

            var server = new HttpListenerServer($"http://+:8888/");
            server.Run(app);
        }

        static Response Home(IRequest request)
        {
            return new TemplatedResponse("home", null);
        }

        static Response Start(IRequest request)
        {
            if (request.Method == "GET")
            {
                var participant = Participants.GetBySession(request.Session.Key);
                return new TemplatedResponse("start", new
                {
                    Participant = participant
                });
            }

            if (request.Method == "POST")
            {
                try
                {
                    var p = new Participant()
                    {
                        Session = request.Session.Key,
                        Name = request.PostArgs["name"],
                        Age = Convert.ToInt32(request.PostArgs["age"]),
                        Allow = request.PostArgs["allow"],
                        Gender = Convert.ToInt32(request.PostArgs["gender"]),
                    };

                    Participants.Add(p);
                }
                catch (Exception)
                {
                    return new RedirectResponse("/start");
                }
                
            }

            return new RedirectResponse("/test/" + TestsManager.Tests.First().Id);
        }

        static Response Test(IRequest request, string[] args)
        {
            // Participant required
            var participant = Participants.GetBySession(request.Session.Key);
            if (participant == null)
                return new RedirectResponse("/start");

            var test = TestsManager.GetById(args[0]);
            if(test == null)
                throw new InvalidOperationException("No such test");

            var nextTest = TestsManager.GetNextFor(test);
            var nextUrl = "/result";
            if (nextTest != null)
                nextUrl = "/test/" + nextTest.Id;

            if (request.Method == "GET")
            {
                return new TemplatedResponse("test", new
                {
                    Test = (Test)test,
                    Participant = participant,
                    NextUrl = nextUrl
                });
            }

            if (request.Method == "POST")
            {
                // Save results
                test.Save(TestsManager.BaseFolder, participant, request);

                Console.WriteLine("Files: " + request.Files.Count());
                return new HttpResponse("OK");
            }

            throw new InvalidOperationException("Unknown method");
        }

        static Response Result(IRequest request)
        {
            // Participant required
            var participant = Participants.GetBySession(request.Session.Key);
            if (participant == null)
                return new RedirectResponse("/start");

            return new TemplatedResponse("results", new
            {
                Results = 123,
                Participant = participant
            });
        }
    }
}
