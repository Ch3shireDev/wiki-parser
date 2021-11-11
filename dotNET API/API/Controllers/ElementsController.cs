using System.Collections.Generic;
using API.Models;
using API.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace API.Controllers
{
    [ApiController]
    [Route("/api/[controller]")]
    public class ElementsController : ControllerBase
    {
        private readonly IElementsService _elementsService;
        private readonly ILogger<ElementsController> _logger;

        public ElementsController(ILogger<ElementsController> logger, IElementsService elementsService)
        {
            _logger = logger;
            _elementsService = elementsService;
        }

        [HttpGet]
        public IActionResult Get(string selectedTypes, string selectedTags)
        {
            var @params = new ElementStringParams
            {
                Tags = selectedTags?.Split(','),
                Types = selectedTypes?.Split(',')
            };
            var result = _elementsService.GetData(@params);
            return Ok(result);
        }
    }

    
}