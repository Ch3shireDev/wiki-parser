namespace API.Services
{
    public interface IElementsService
    {
        ElementsServiceParams GetData(ElementStringParams parameters = null);
    }
}